#template, needs to be changed and modified. inputed as exmaple

# Importing Required libraries

import os
import json
import openai
import logging
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from threading import Thread
from dash import Dash, html, dcc
from uagents_core.crypto import Identity
#from fetchai.crypto import Identity
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app for webhook
flask_app = Flask(__name__)

# Dash app with Bootstrap theme
dash_app = Dash(
    __name__,
    server=flask_app,
    url_base_pathname='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]  # Bootstrap theme
)

# Identity for the agent
analytics_identity = None
graphs = []

# Initialize OpenAI API key
openai.api_key = "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" #os.getenv("OPENAI_API_KEY")#OPENAI_API_KEY

# Function to generate visualization suggestions on given dataframe and number of suggestions
def get_visualization_suggestions(dataframe, num_suggestions):
    
    columns = ', '.join(dataframe.columns) # column names as a string

    prompt = (
        f"Given the following dataset columns: {columns}, "
        f"suggest {num_suggestions} of the most insightful visualizations for comprehensive data analysis. "
        "For each suggestion, specify the column(s) involved and the type of visualization. "
        "Use only the following visualization types: 'scatter', 'pie chart'. "
        "Ensure that the number of columns specified matches the requirements for each visualization type: "
        "use exactly two columns for 'scatter' charts; use exactly one column for 'pie chart'. "
        "Format the output as a JSON array of objects, each containing 'columns' (a list of column names) and 'type' (the visualization type)."
        f"Here is the info of df {dataframe.info()} and description of data {dataframe.describe()} to get better understanding of data."
    )
    # Making an openai chat completions call to get suggestions
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        response_content = response.choices[0].message.content.strip()
        logger.info(f"Raw response from OpenAI: {response_content}")

        # Remove markdown formatting characters if present
        cleaned_response = response_content
        if response_content.startswith("```json"):
            cleaned_response = response_content.strip("```json").strip("```").strip()
        elif response_content.startswith("```"):
            cleaned_response = response_content.strip("```").strip()

        # Attempt to parse the response
        try:
            suggestions = json.loads(cleaned_response)
            logger.info(f"Visualization suggestions: {suggestions}")
            return suggestions
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON parsing error: {json_err}")
            logger.error(f"Failed to parse cleaned response: {cleaned_response}")
            return []
    except Exception as e:
        logger.error(f"Error getting visualization suggestions: {e}")
        return []

# Flask route to handle webhook or messages to the agent
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    global graphs
    global analytics_identity
    try:
        # Parse the incoming message
        data = request.get_data().decode('utf-8')
        message = parse_message_from_agent(data)
        data_path = message.payload.get("data_path", "")
        agent_address = message.sender

        if not data_path:
            return jsonify({"status": "error", "message": "No data path provided"}), 400

        # Load dataset
        logger.info(f"Loading dataset from: {data_path}")
        try:
            df = pd.read_csv(data_path)
            df.columns = df.columns.str.strip()
            logger.info(f"Dataset columns: {df.columns}")
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return jsonify({"status": "error", "message": "Failed to load dataset"}), 500

        # Get visualization suggestions
        suggestions = get_visualization_suggestions(df, 7)

        # Generate graphs for Dash
        graphs.clear() #clearing graphs before generation
        for suggestion in suggestions:
            cols = suggestion.get('columns', [])
            graph_type = suggestion.get('type', '').lower()

            if graph_type == 'scatter' and len(cols) == 2:
                fig = px.scatter(df, x=cols[0], y=cols[1], title=f'Scatter Plot: {cols[0]} vs {cols[1]}')
                graphs.append(dbc.Card([
                    dbc.CardHeader(f"Scatter Plot: {cols[0]} vs {cols[1]}"),
                    dbc.CardBody(dcc.Graph(figure=fig))
                ], className="mb-4"))
            elif graph_type == 'pie chart' and len(cols) == 1:
                fig = px.pie(df, names=cols[0], title=f'Pie Chart of {cols[0]}')
                graphs.append(dbc.Card([
                    dbc.CardHeader(f"Pie Chart of {cols[0]}"),
                    dbc.CardBody(dcc.Graph(figure=fig))
                ], className="mb-4"))
            else:
                logger.warning(f"Unrecognized suggestion: {suggestion}")

        if not graphs:
            logger.error("No graphs generated.")
            return jsonify({"status": "error", "message": "No valid visualizations generated"}), 500

        # Refresh Dash layout
        dash_app.layout = dbc.Container([
            html.H1("Data Visualizations Dashboard", className="my-4"),
            html.P("Explore visualizations generated for your dataset.", className="lead"),
            dbc.Row(graphs),
            html.Footer("Powered by Fetch.ai & OpenAI", className="text-center mt-4")
        ], fluid=True)

        # send the dashboard URL to frontend client and response.
        dashboard_url = f"http://{request.host}/dashboard/"
        payload = {'dashboard_url' : dashboard_url}
        send_message_to_agent(
            analytics_identity,
            agent_address,
            payload
        )
        return jsonify({"status": "graphs_sent"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Initialize Dash layout
def init_dash_app():
    dash_app.layout = dbc.Container([
        html.H1("Data Visualizations Dashboard", className="my-4"),
        html.P("No visualizations generated yet. Submit a dataset to generate insights.", className="lead")
    ], fluid=True)

# Initialize the agent
def init_agent():
    global analytics_identity
    try:
        analytics_identity = Identity.from_seed("thisisyourdashboardagentphrase", 0) #os.getenv("DASHBOARD_AGENT_KEY"), 0)#DASHBOARD_AGENT_KEY
        register_with_agentverse(
            identity=analytics_identity,
            url="http://localhost:5008/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),#AGENTVERSE_API_KEY
                                    
            agent_title="Dashboard Analytics Agent",
            # Define the client agent's metadata
            readme = """
                <description>Dasboard agent to create dashboard for the given data set.</description>
                <use_cases>
                    <use_case>Create dashboard with different scatter and pie plots for given structured data.</use_case>
                </use_cases>
                <payload_requirements>
                <description>Expects the path for the dataset.</description>
                    <payload>
                        <requirement>
                            <parameter>data_path</parameter>
                            <description>Path to the dataset for dashbpard creation</description>
                        </requirement>
                    </payload>
                </payload_requirements>
            """
        )
        logger.info("Analytics agent registered successfully!")
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        raise

# Run Flask and Dash servers
if __name__ == "__main__":
    init_dash_app()
    init_agent()
    load_dotenv()
    print("thisisyouragentphrase") #os.getenv("CLIENT_KEY"))#CLIENT_KEY
    # Run Flask in a separate thread
    Thread(target=lambda: flask_app.run(host="0.0.0.0", port=5008, debug=True, use_reloader=False)).start()

