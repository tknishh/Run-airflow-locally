# Run-Airflow-locally

Often it proves difficult to run airflow on a windows machine. Docker is the easiest way to run airflow locally.

Follow the below steps to run Jupyter and Airflow locally using docker.

# Download Docker Desktop

Use the following link to download [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

# Step 1 - Create a python virtual environment
Open Terminal (Powershell)

Run the following commands

`python -m venv dp`

`dp/Scripts/activate`

# Step 2 - Install and initialize phidata

Install   
`pip install phidata`

Initialize   
`phi init -l`

Login in phidata using google account or github as per your convinience

# step 3 - Create a Workspace

Create a workspace in directory to store all the data product code.

`phi ws init`

Provide a name to the workspace and select the template to work on.

## Running the workspace
`phi ws up`

# Step 5: Open the Jupyter UI

Open [localhot:8888](localhost:8888) in a new tab to view the jupyterlab UI.

### Password: admin

Open notebooks/examples/crypto_nb.ipynb and run all cells using Run → Run All Cells

This will download crypto prices and store them in a CSV Table at storage/tables/crypto_prices

# Step 6: Run Airflow
Open the workspace/settings.py file and uncomment dev_airflow_enabled=True (line 19). Start the workspace using

`phi ws up`
Press Enter to confirm. Give about 5 minutes for the containers to run and database to initialize. Check progress using: docker logs -f airflow-scheduler-container

# Step 7: Open the Airflow UI
Open localhost:8310 in a new tab to view the Airflow UI.

### User: admin

### Pass: admin

# Step 8: Run workflow using Airflow
Switch ON the crypto_prices DAG which contains the same task as the crypto_nb.ipynb notebook, but as a daily workflow.

Checkout the workflows/crypto/prices.py file for the full code. The table is written to the storage/tables/crypto_prices directory.

# Step 9: Play around
Play around, create notebooks, DAGs and read more about phidata

# Step 10: Shut down
Stop the workspace using

`phi ws down`


