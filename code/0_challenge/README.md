# Challenge 0: Environment Setup

If you’re running this workshop on your own, you'll need to deploy the workshop resources to your Azure subscription. Follow the instructions to deploy the workshop resources.

## Overview
We will set up the initial environment for you to build on top of during your Microhack. This comprehensive setup includes configuring essential Azure services and ensuring access to all necessary resources. Participants will familiarize themselves with the architecture, gaining insights into how various components interact to create a cohesive solution. With the foundational environment in place, the focus will shift seamlessly to the first Microhack Challenge endeavor.

## Prerequisites

1. A computer running Windows 11, macOS, or Linux.
1. An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/){:target="_blank"} before you begin.
1. Install the [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli){:target="_blank"}.
1. Install [Powershell 7 (supported on Windows, macOS, and Linux)](https://learn.microsoft.com/powershell/scripting/install/installing-powershell){:target="_blank"}.
1. Install [Python 3.13+](https://www.python.org/downloads/){:target="_blank"}.
1. Install the Git CLI. You can download it from the [Git website](https://git-scm.com/downloads){:target="_blank"}.

## Support Software
* Azure Developer CLI: Download azd
* Ensure the correct OS is selected
* Powershell 7+ with AZ module (Windows only): Powershell, AZ Module
* Git: Download Git
* Node.js 16+ windows/mac linux/wsl
* Python 3.11: Download Python

## Recommended Regions

* North Central US (northcentralus)
* South Central US (southcentralus)
* Sweden Central (swedencentral)
* West US (westus)
* West US 3 (westus3)
* East US (eastus)
* East US 2 (eastus2)

See Regional Selection - gpt-4o, 2024-05-13. If you are having issues with the deployment

## Deploy the Azure Resources

1. Open a terminal window.
1. Clone the workshop repo by running the following command:

    ```bash
    git clone https://github.com/gloveboxes/build-your-first-agent-with-azure-ai-agent-service-lab.git
    ```

1. Navigate to the workshop `infra` folder for the repository you cloned in the previous step.

    ```bash
    cd build-your-first-agent-with-azure-ai-agent-service-lab/infra
    ```

1. Run the deployment script with the following command:

    ```bash
    pwsh deploy.ps1
    ```

1. Follow the prompts to deploy the workshop resources to your Azure subscription.

## Run the workshop

After the deployment is complete, follow the steps in the [Lab Introduction](./introduction-self-guided.md) to run the workshop. 

# CHALLENGE 0 COMPLETE!!!!!