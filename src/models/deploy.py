# -*- coding: utf-8 -*-

"""FakeNewsClassifier Deployment

The workflow is similar no matter where you deploy your model:

1. Register the model
2. Prepare an entry script
3. Prepare an inference configuration
4. Deploy the model locally to ensure everything works
5. Choose a compute target
6. Re-deploy the model to the cloud
7. Test the resulting web service
8. For more information on the concepts involved in the machine learning deployment 
   workflow, see Manage, deploy, and monitor models with Azure Machine Learning.

"""
# %% Imports
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
import argparse
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if '__name__' == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Provide deployment args')
    parser.add_argument('--env_name', help='Name of env', type=str)
    parser.add_argument('--reg_model', help='Should the model be newly registered? Default=False' , type=bool, default=False)
    parser.add_argument('--reg_env', help='Should the env be newly registered? Default=False', type=bool, default=False)
    parser.add_argument('--deploy_local', help='Should the service be deployed locally? Default=True', type=bool, default=True)
    args = parser.parse_args()
    # %% Define constants for deployment
    AZURE_CONFIG_PATH = os.getenv('AZURE_CONFIG_PATH')
    MODEL_PATH = os.getenv('MODEL_PATH')
    MODEL_NAME = os.getenv('MODEL_NAME')
    ENV_NAME = os.getenv('ENV_NAME')
    SRC_DIR = os.getenv('SRC_DIR')
    ENTRY_SCRIPT = os.getenv('ENTRY_SCRIPT')
    DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
    LOCAL_PORT = os.getenv('LOCAL_PORT')
    CPU_CORES = os.getenv('CPU_CORES')
    MEMORY_GB = os.getenv('MEMORY_GB')
    # %% Connect to Azure workspace from config.json
    ws = Workspace.from_config(AZURE_CONFIG_PATH)
    logging.info('Successfully connected to Azure Workspace')
    # %% Regeister model in workspace
    if args.reg_model:
        model = Model.register(workspace=ws,
                            model_path=MODEL_PATH,
                            model_name=MODEL_NAME)

    model = Model(ws, MODEL_NAME)

    # %% Create conda and pip dependencies for inferencing
    conda_packages = ['python=3.8.8',
                    'scikit-learn=1.0',
                    'pandas=1.3.4',
                    'catboost=0.26.1',
                    'nltk=3.6.5']
    pip_packages = ['azureml-core',
                    'azureml-defaults']

    # Create env with conda and pip dependencies
    env = Environment(name=ENV_NAME)
    cd = CondaDependencies.create(pip_packages=pip_packages, conda_packages=conda_packages)
    env.python.conda_dependencies = cd

    #env.save_to_directory('./newenvfile')
    # %% Create inference config
    inference_config = InferenceConfig(environment=env,
                                    source_directory=SRC_DIR,
                                    entry_script=ENTRY_SCRIPT)

    #%% Register environment to re-use later
    if args.reg_env:
        env.register(workspace = ws)
        logger.info('Registered environment')
    # %% Define deployment configuration

    # First deploy it locally
    if args.deploy_local:
        deployment_config = LocalWebservice.deploy_configuration(port=LOCAL_PORT)

    deployment_config = AciWebservice.deploy_configuration(
                cpu_cores=CPU_CORES,
                memory_gb=MEMORY_GB)

    #%% Deploy model
    service = Model.deploy(
        workspace=ws,
        name=DEPLOYMENT_NAME,
        models=[model],
        inference_config=inference_config,
        deployment_config=deployment_config,
        overwrite=True,
    )
    service.wait_for_deployment(show_output=True)
    logging.info(service.get_logs())
    logging.info('Inference endpoint is running on: %s' % service.scoring_uri)
