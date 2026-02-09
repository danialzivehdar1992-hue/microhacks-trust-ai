# Challenge 1: Responsible AI - Designing a Reliable & Ethical Approach

## Overview

Contoso Electronics is piloting an internal HR Q&A application where employees can ask about benefits and policies. The chat agent retrieves answers from policy documents with citations. Chat applications are typically graded on functionality and not on the impact on end-users. We want to help developers and sponsors gain trust in their applications in the early stages of the development cycle while gaining confidence in its feasibility. In this challenge, we will work in the Planning phase to prototype our application through model selection, context engineering, and manual evaluation. The purpose of the planning phase is to green light our concept into a working application and understand its strengths and limitations to better design it for the Build Phase.
<br>

## Tools & Config Needed

1. Microsoft Foundry Classic Portal (General Available)

1. Azure AI Search (Indexed Data)

1. Azure OpenAI model deployment (GPT-4.1-mini, GPT-4o and text-embedding-3-large)

1. Ground truth Q&A list (JSONL file or Synthetic Data Generation)

---
<br>

## Key Tasks for Challenge

- Review models in model catalog to ensure best models deployed to your environment for your specific use case
- Configure chat playground to leverage the best data (context) for your application
- Experiment in Chat Playground with ground truth data and manually evaluate results
- Conduct Impact Assessment to ensure AI behaves responsibly and ownership and metrics are identified to mitigate risk
- Build guardrails in Playground to enforce safety, groundedness and prompt protections

---
<br>

## Lab Activities

## Lab 1 – Microsoft Foundry Agent Playground

Business users and developers have been working conceptually on a use case but are not certain how the Large Language Model (LLM) will respond to user input. In the planning phase, we want to quickly set up an environment to determine feasibility and evaluate the quality of the responses. Microsoft Foundry provides the Agent Playground, where you can set up the agent, connect it to Azure AI Search, and send test questions into the chat interface to see the LLM responses. This first lab will be a set of instructions on how to set up the environment and input your ground truth questions to determine feasibility in the platform and confidence in the responses.

### Key Tasks

- Review models in model catalog to ensure best models deployed to your environment for your specific use case
- Configure chat playground to leverage the best data (context) for your application
- Experiment in Chat Playground with ground truth data and manually evaluate results

---

### Lab 1.1.1 – Instructions for Model Selection

1. Go into the Foundry project via the Azure Portal

    ![Alt text](/media/CH1_Foundry.png "Foundry Project")

1. Ensure your Foundry portal is in classic mode and you are at the Foundry project interface.  

    ![Alt text](/media/CH1_FoundryClassic.png "Foundry Project Classic")

1. Click on Model Catalog to inspect the models available to you.  For this Microhack we are leveraging three models, gpt-4.1-mini, gpt-4o and text-embedding-3-large.  Go into model catalog to review their model cards to understand what use cases they support.  Click on details and go into benchmarks.

    ![Alt text](/media/CH1_MCatalog.png "Foundry Model Catalog")

1. For benchmarks tab, click on ```Compare with more models``` and remove all models that are not part of this hack and add the extra one that is missing. The benchmark chart should look like this.

    ![Alt text](/media/CH1_Benchmarks.png "Model Benchmarks")

1. Identify which model will be used for model evaluations, chat application and search engine based on the results of this benchmark test and why based on capabilities.

    ![Alt text](/media/CH1_ModelGrid.png "Model Grid")

---

### Lab 1.1.2 – Instructions for Agent Evaluation

1. Go to the command line terminal in codespaces and submit this script to build an agent.  

    ```bash
    python ./scripts/03_create_agent.py
    ```

1. Click on Playgrounds and select the Agent playground from the menus

    ![Alt text](/media/CH1_Playground.png "Agent Playground")

1. A screen will appear called Agent Playground.  Select the gpt-4.1-mini model for your chat application as discussed in model selection.

    ![Alt text](/media/Ch1_modeldeployment.png "Model Deployment")

1. Define the system message for the Agent in the Instructions section.  A good example is ```You must answer only HR benefits—related questions such as leave policies, PTO, parental leave, insurance, perks, holidays, and HR processes.```

1. Setup the knowledge base by clicking the Add button.  You will want to leverage Azure AI Search as the data source.  

    ![Alt text](/media/CH1_knowledgebase.png "Azure Search")

1. Lastly, it will ask you to connect to an index already in the project.  There is only one option for Project index and for Search type choose semantic.  The reason for one option is due to the project connections.  Please name the index ```hrdocs```

    ![Alt text](/media/CH1_IndexSetup.png "IndexSetup")

1. Test your agent- Ask some sample questions, available here - (https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/evals/ground_truth.jsonl)

    ![Alt text](/media/CH1_Agentchat.png "Agent Chat")

1. Compare the results with your ground truth data to see if agent is able to answer your questions sufficiently.  There is also an AI quality score for coherence, fluency and relevance which an AI Judge scores and provides a reason code in the Agent Playground.

    ![Alt text](/media/CH_1_Agent_Manual_eval.png "Agent Playground Eval Score")

1. Click on View Run Info button next to Tools in the same menu as AI quality.  This will share the thread for the question.  On the far right click on the evaluations header to see the actual score for each quality evaluator and an explanation.  Run a few questions to see if you have the right model and the results are acceptable.  This helps you run manual evaluations to approve your prototype for development.

    ![Alt text](/media/CH_Trace_eval.png "Agent Score & Reason code in Trace")

---

<br>

## Lab 1.2 – Responsible AI Impact Assessment

Early in the Planning phase, an [Impact Assessment](https://msblogs.thesourcemediaassets.com/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf) helps govern the Generative AI application. In this lab, an example Impact assessment is shared with you to review.  Review the assessment and for each risk identify the quality or safety metrics that are in scope.

Conducting this Responsible AI Impact Assessment not only mitigates risks but also builds confidence among stakeholders and users. Employees will trust the HR assistant more knowing it’s been thoughtfully vetted, and your organization can deploy it knowing that ethical and legal considerations have been addressed up front. This thorough, proactive approach exemplifies Responsible AI in practice – delivering the benefits of AI (quick HR answers and improved productivity) while minimizing potential downsides through careful planning and oversight.  Now that the Impact Assessment is drafted with risks and mitigations, it needs to be reviewed and signed off by the appropriate stakeholders before the HR assistant goes live. Once the Impact Assessment is approved, the next step is to validate the agent’s real-world performance through manual evaluation.

---

### Lab 1.2.1 – Instructions

* There are four risks in the impact assessment.  Review each risk and compare them against the [quality & safety metrics](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability?view=foundry-classic#what-are-evaluators) setup in Foundry as evaluators.  This workflow will help you in the BUILD phase to setup evaluations and monitors to ensure the application is in compliance with your standards.

---

#### Impact Assessment Sample

1. Identified Risk: Outdated or incorrect policy info (agent might give obsolete answers if documents aren’t updated)

	Mitigation Strategy
	* Schedule regular updates of the HR policy index (e.g., after any HR policy change).
	* Implement a content update checklist with HR team for new/changed policies.– Include policy last-updated timestamps in answers, if feasible, to flag potentially old info.

	Owner Accountable
	* HR Knowledge Manager (ensures documents & index stay current)	

2. Identified Risk: Biased or uneven answers (e.g., gendered language or differing info for different groups)

	Mitigation Strategy:
	* Review and revise policy wording for inclusive language (e.g., use “primary caregiver” instead of “mother”).
	* Add system prompt guidance to use neutral tone and equal detail for all users.– Test with diverse query phrasing (male vs female perspective, etc.) and verify consistent responses.

	Owner Accountable:
	* AI Developer (updates prompts & tests); HR Policy Analyst (reviews content for bias)	

3. Identified Risk: Personal data exposure (user asks for individual’s info or system reveals PII)

	Mitigation Strategy:	
	* Restrict knowledge sources to non-PII documents only (no personal files indexed).
	* Model instructed to refuse requests for personal/sensitive data.
	* Enable content filter/DLP for PII (e.g., detect patterns like SSN, phone # in outputs).– Test queries asking for private data to ensure the agent safely refuses.

	Owner Accountable:
	* Solution Architect / Privacy Officer (ensures data scope and compliance)

4. Identified Risk: Misuse or unsafe requests (attempts to get the bot to violate policies or produce harmful content)

	Mitigation Strategy:	
	* Employ Azure AI Content Safety and Foundry guardrails (already active) to block disallowed content.
	* Keep system and safety prompts in place to enforce refusals for out-of-scope questions.
	* Conduct red-team testing (prompt injections, extreme inputs) and adjust safeguards if any gap is found.– Log and review misuse attempts to continuously improve defenses.

	Owner Accountable:
	* AI Engineering Lead (sets guardrail configs and reviews security logs)	

---

<br>

## Lab 1.3 – Guardrails and Evaluations

### Objective

Configure guardrail policies and run automated evaluations in Microsoft Foundry to ensure your Agent operates safely, complies with organizational standards, and delivers accurate, grounded, and reliable responses before deployment.

### Key Tasks

- Create a Guardrail Policy using Foundry’s Compliance workspace to enforce content safety filters, prompt shields, and groundedness checks.
- Configure policy scope and exceptions at the subscription or resource group level to control which model deployments must comply.
- Run an automated evaluation job to measure relevance, groundedness, safety, and policy compliance of the Agent’s responses.
- Analyze evaluation metrics and results, including failed cases, reasoning traces, and quality indicators.

---

### Lab 1.3.1 – Instructions

1. Create a guardrail policy- https://learn.microsoft.com/en-us/azure/ai-foundry/control-plane/quickstart-create-guardrail-policy?view=foundry&viewFallbackFrom=foundry-classic

    ![Alt text](/media/CH1_Operate.png "Guardrails")

1. Click on ```Content Filters``` above the Guardrails and controls banner. Click the Create content filter button

    ![Alt text](/media/CH1_ContentFilter.png "ContentFilter")

1. Setup the Content filter thru the wizard.  It will ask you for Input filters, output filters and connection.  Review and accept the default settings. Here is a review of the setup. Click Create filter

    ![Alt text](/media/CH1_Reviews.png "ContentFilterReview")

---

## Success Criteria

To successfully complete this lab, you must meet all of the following criteria:

1. Create and activate a Foundry agent in the playground connected to Azure AI Search.

1. Type in a few questions for manual evaluation and judge them.

1. Identify the metrics for each risk in the Impact Assessment. [Answer Key](/docs/RAIkey.md)

1. Apply a Guardrail Policy enforcing safety, groundedness, and prompt protections.

## Continue to Challenge 2

Congratulations for completing Challenge 1 on Responsible AI.  Next challenge is [Challenge 2 (Well-Architected & Trustworthy Foundation)](/code/2_challenge/README.md).

## Best Practices

As we wrap up the prototyping phase for Microsoft Foundry projects, the guiding principle is to build purposeful, decision-aligned prototypes that reveal real business value and risk before any broader rollout. That means keeping the scope narrowly defined and explicitly tied to a concrete business outcome, using enterprise retrieval such as Azure AI Search to ground responses in authoritative knowledge rather than relying on static prompt content, and writing clear system instructions that guide model behavior and reduce hallucinations. Guardrail policies — including safety, groundedness, and prompt shields — should be configured early to ensure the model meets enterprise safety and compliance expectations, and prototypes should be evaluated against both typical cases and edge or failure cases with ground-truth datasets. Treat governance, systematic testing, and observability not as post-deployment tasks but as first-class features from day one, leveraging Foundry’s built-in observability and evaluation tools to continuously monitor quality, performance, and risks. By embedding these practices into prototyping, teams not only improve output reliability and trust, but also build a solid foundation for scaling toward production-grade AI solutions


## Learning Resources

[Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry?view=foundry-classic)

[Microsoft Foundry Control Plane](https://learn.microsoft.com/en-us/azure/ai-foundry/control-plane/overview?view=foundry)
 
[Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search?tabs=indexing%2Cquickstarts)

[Impact Assessment](https://www.microsoft.com/en-us/ai/tools-practices)

[Responsible AI](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai?view=azureml-api-2)

 
#  CHALLENGE 1 COMPLETE !!!