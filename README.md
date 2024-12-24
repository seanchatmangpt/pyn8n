# pyn8n v4

**pyn8n** is an advanced Python client and automation toolkit designed to extend and enhance the functionality of [n8n](https://n8n.io). This new release introduces **dynamic integration capabilities**, **conversational automation tools**, and a seamless **developer experience** for orchestrating workflows with Python. It integrates directly with n8n while leveraging Python's flexibility to tackle advanced use cases, ensuring a smooth, efficient, and scalable automation process.

---

## 🚀 Features

- **Dynamic Workflow Generation**: Create, manage, and monitor workflows programmatically using a Pythonic API.
- **Conversational CLI**: Use natural language to define workflows with an interactive CLI powered by AI.
- **Ash Framework Integration**: Enable advanced orchestration and business logic layers with Ash while remaining invisible to n8n automators.
- **n8n API Wrapper**: Simplified and robust interaction with n8n’s REST APIs, including node discovery and dynamic updates.
- **Plug-and-Play Extensibility**: Add custom nodes, integrations, and pre-built actions with minimal setup.
- **Enterprise-Grade Governance**: Monitor workflows, track execution logs, and implement error handling for compliance-ready automation.

---

## 🛠️ Installation

To install pyn8n, run:

```bash
pip install pyn8n
```

---

## 🔧 Configuration

### Prerequisites

1. **n8n Instance**: Ensure you have an n8n instance running locally or hosted.
2. **API Key**: Generate an API key in your n8n settings for secure access.

### Environment Variables

Create a `.env` file in your project directory with the following:

```env
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_api_key_here
```

Or set them directly in your environment.

---

## 📚 Usage

### CLI

Run the following command to start the interactive CLI:

```bash
pyn8n
```

Example:

```bash
$ pyn8n
Welcome to pyn8n! What would you like to automate today?
> Send an email when a new row is added to Google Sheets.
> Generating workflow...
> Workflow created! Would you like to run it now? (yes/no)
```

### Python API

#### Creating a Workflow

```python
from pyn8n import N8nClient, Workflow

# Initialize client
client = N8nClient(base_url="http://localhost:5678", api_key="your_api_key")

# Define a workflow
workflow = Workflow(
    name="New Row Email Notification",
    nodes=[
        {
            "id": "1",
            "type": "trigger",
            "parameters": {"sheet": "ExampleSheet"},
            "position": [200, 150],
        },
        {
            "id": "2",
            "type": "email",
            "parameters": {"recipient": "user@example.com", "message": "New row added!"},
            "position": [400, 150],
        },
    ],
    connections={"1": ["2"]},
)

# Create and activate workflow
created_workflow = client.create_workflow(workflow)
client.activate_workflow(created_workflow.id)
```

#### Managing Credentials

```python
from pyn8n import Credential

# Add credentials
client.create_credential(Credential(name="Google Sheets API", type="google", data={"api_key": "your_google_api_key"}))
```

---

## 🧑‍💻 Development

### Running Locally

Clone the repository and start a development environment:

```bash
git clone https://github.com/user/seanchatmangpt/pyn8n.git
cd pyn8n

# Using Docker
docker compose up --detach dev
docker compose exec dev zsh

# Or, using Codespaces or VS Code Dev Containers
```

### Testing

Run tests with:

```bash
poe test
```

---

## 🤝 Contributing

We welcome contributions! Follow these steps to get started:

1. Fork the repository and create a new branch for your changes.
2. Run `poe lint` to check code style.
3. Submit a pull request with a detailed description of your changes.

For detailed contribution guidelines, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 🌟 Features in v4

1. **Dynamic Node Mapping**: Automatically generate and sync node configurations based on n8n instances.
2. **Ash Framework Backend**: Optional integration for handling state machines, advanced orchestration, and resource management.
3. **Enterprise Integrations**: Extend n8n workflows with enterprise-grade observability and governance.
4. **Error Handling and Retries**: Built-in support for managing failed executions with fallback strategies.
5. **Interactive Workflow Creation**: Use natural language or the Python API to define workflows programmatically.

---

## 💼 For Enterprises

For enterprise users, pyn8n offers support for:

- **Role-based Access Control (RBAC)**
- **Custom Node Libraries**
- **Advanced Logging and Monitoring**
- **Dedicated Support and SLAs**

Contact us at [enterprise@pyn8n.io](mailto:enterprise@pyn8n.io) for more details.

---

## 🛣️ Roadmap

- [ ] **AI-Assisted Workflow Suggestions**  
- [ ] **Marketplace Integration for Pre-Built Workflows**  
- [ ] **Advanced Analytics Dashboards**  
- [ ] **Cross-Platform Automation**

---

## 📜 License

pyn8n is released under the [MIT License](LICENSE).  

Happy automating! 🚀