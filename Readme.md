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



# Run Airflow Locally

