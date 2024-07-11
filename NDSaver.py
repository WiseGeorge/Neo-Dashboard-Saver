import json
import os
import uuid
import logging
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class NDashboardSaver:
    """
    A service class for interacting with a Neo4j database to save neodash dashboard data.

    Attributes:
        uri (str): The URI of the Neo4j database.
        user (str): The username for Neo4j authentication.
        password (str): The password for Neo4j authentication.
        dashboard_path (str): The path to the JSON dashboard file.
        logger (logging.Logger): The logger for this class.
    """

    def __init__(self, uri=os.environ.get('NEO_URL'), user=os.environ.get('NEO_USER'), password=os.environ.get('NEO_PWD'), dashboard_path=os.environ.get('DASHBOARD_PATH')):
        """
        Initializes the DashboardSaver with the provided URI, username, password, and dashboard path.

        Args:
            uri (str): The URI of the Neo4j database.
            user (str): The username for Neo4j authentication.
            password (str): The password for Neo4j authentication.
            dashboard_path (str): The path to the JSON dashboard file.
        """
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.dashboard_path = dashboard_path
        self.user = user
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def close(self):
        """Closes the connection to the Neo4j database."""
        self._driver.close()

    def create_node(self, label, data, user):
        """
        Creates a node in the Neo4j database with the given label and data.

        Args:
            label (str): The label for the node.
            data (dict): The data to store in the node.
            user (str): The user creating the node.

        Returns:
            int: The ID of the created node.
        """
        self.logger.info('Creating a node in the Neo4j database.')
        try:
            with self._driver.session() as session:
                node_id = session.execute_write(self._create_node, label, data, user)
                self.logger.info(f'Node created:\n {node_id}')
                return node_id
        except Exception as e:
            self.logger.error('Failed to create a node in the Neo4j database.', exc_info=True)
            raise e

    @staticmethod
    def _create_node(tx, label, data, user):
        """
        A static method to create a node in a transaction.

        Args:
            tx (neo4j.Transaction): The transaction object.
            label (str): The label for the node.
            data (dict): The data to store in the node.
            user (str): The user creating the node.

        Returns:
            int: The ID of the created node.
        """
        date = datetime.now().isoformat()
        uuid_str = str(uuid.uuid4())
        title = data.get('title', '')
        version = data.get('version', '')
        content = json.dumps(data)
        query = (
            f"CREATE (a:{label} {{date: $date, title: $title, user: $user, uuid: $uuid, version: $version}}) "
            "RETURN a"
        )
        result = tx.run(query, content=content, date=date, title=title, user=user, uuid=uuid_str, version=version)
        node = result.single()[0]
        return json.dumps(dict(node), indent=4)

    def load_json(self):
        """
        Loads JSON data from a file.

        Returns:
            dict: The JSON data loaded from the file.
        """
        self.logger.info('Loading JSON data from a file.')
        try:
            with open(self.dashboard_path, 'r', encoding='utf8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            self.logger.error('Failed to load JSON data from a file.', exc_info=True)
            raise e

    def init_save(self):
        """
        The main function to run the script. It connects to the Neo4j database,
        loads JSON data from a specified file, and creates a node with that data.
        """
        # Load JSON data from the specified file
        data = self.load_json()

        # Label for the node
        label = '_Neodash_Dashboard'

        # Create the node in the Neo4j database
        self.create_node(label, data, self.user)

        # Close the DashboardSaver service connection
        self.close()

if __name__ == "__main__":
    dashboard_saver = NDashboardSaver()
    dashboard_saver.init_save()
