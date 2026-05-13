# 🛠️ Installation & Setup

Follow these steps to get your local instance of **Xpos3** up and running.

---

### 📦 Step 1: Install Required Software
The system relies on a containerized environment and a local LLM. Ensure the following are installed:

| Software | Purpose | Link |
| :--- | :--- | :--- |
| **Docker Desktop** | Container Management | [Download](https://www.docker.com/products/docker-desktop/) |
| **Git** | Version Control | [Download](https://git-scm.com/) |
| **Ollama** | Local LLM Engine | [Download](https://ollama.com/) |

> [!IMPORTANT]  
> **Ollama** must be active before starting the containers. Once installed, pull the required model:
> ```bash
> ollama pull gemma2:2b
> ```

---

### 📂 Step 2: Clone the Project
Run the following commands in your terminal to download the repository and enter the project directory:

```bash
# Clone the repository
git clone [https://github.com/LujainAlabbad/Xpos3.git](https://github.com/LujainAlabbad/Xpos3.git)

# Navigate to the project folder
cd Xpos3
```
### 🎨 Step 2.5: Install Frontend Dependencies

Since the `node_modules` folder is excluded from the repository, you must install the required packages locally before running the frontend.

Navigate to the frontend directory and run:

```bash
cd frontend
npm install
```
### ⚙️ Step 3: Configure Environment Variables

To ensure secure communication and database access, you must set up your environment variables. 

1. Create a file named `.env` in the root directory.
2. Copy the following template into the file:

```ini
# Database Configuration
POSTGRES_PASSWORD=secure_password

# Security Keys
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

# LLM Configuration (Left empty for local Ollama use)
OPENAI_API_KEY=
```
### 🚀 Step 4: Launch the System

Once the software is installed and the `.env` file is configured, you can launch the entire system using Docker. Run the following command in your terminal:

```bash
docker-compose up --build
```
> [!SUCCESS]
> **Congratulations!** Your system is now running. You can access the dashboard by navigating to `http://localhost:3000` (or your configured frontend port) in your web browser.
