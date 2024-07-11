# 🚀 NDashboardSaver: Automating NeoDash Dashboard Deployment

NDashboardSaver is a Python class designed to automate the process of saving NeoDash dashboards in Neo4j. This tool simplifies the deployment of dashboards to production environments, enhancing efficiency and productivity.

## 🌟 Features

* **Automated Saving** : No more manual saving of dashboards every time you need to deploy or restart your system.
* **Ease of Use** : Simply set up your Neo4j connection configurations and the path to your NeoDash JSON dashboard file in the environment variables, and you’re good to go.
* **Efficiency** : Streamlines the process of deploying dashboards to production environments.

## 📚 Usage

```python
# Import
from NDSaver import NDashboardSaver

# Initialize the NDashboardSaver service
dashboard_saver = NDashboardSaver()

# Load JSON data and save the dashboard to Neo4j
dashboard_saver.init_save()
```

With this, you only need to create an instance of `NDashboardSaver` and call the `init_save` method. This method will load the JSON data from the specified file and save the dashboard to the Neo4j database. It’s as simple as that! 🎉

## ⚙️ Configuration

Set the following environment variables:

```env
NEO_URL=bolt://localhost:7687
NEO_USER=neo4j
NEO_PWD=password
DASHBOARD_PATH=path/to/dashboard.json
```

## 🔗 Useful Links

* [NeoDash](https://github.com/neo4j-labs/neodash)
* [Neo4j ](https://neo4j.com/)

With `NDashboardSaver`, deploying your NeoDash dashboards to production is now a breeze

A Python class designed to streamline the process of saving NeoDash dashboards in Neo4j simplifying the automation of deploying dashboards to production environments.

## 🖼️Gallery Examples

The dashboard example featured in the gallery is sourced from the Neodash repository. All credit for the gallery content goes to the developers and contributors of Neodash.
