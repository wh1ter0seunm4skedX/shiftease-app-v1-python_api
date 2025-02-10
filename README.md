# ShiftEase

A modern event management system designed to streamline coordination and engagement for **youth workers** at community centers.

---

### **Overview**

**ShiftEase** is a full-stack web application built to make managing events and coordinating **youth workers** in community centers seamless and efficient. Whether you're scheduling shifts or tracking participation, ShiftEase provides an intuitive interface that helps your team stay organized and connected, while keeping the process smooth for both administrators and workers.

---

### **Features**

- **User Authentication**: Secure login and registration with role-based access control to ensure everyone has the right permissions.
- **Event Management**: Create, update, and delete events with detailed descriptions, times, and tasks for youth workers.
- **Youth Worker Coordination**: Track availability, participation, and shifts to ensure every event is fully staffed and supported.
- **Real-time Updates**: Get instant notifications for event changes and shift registrations, so everyone stays in the loop.
- **Responsive Design**: Works flawlessly on both desktop and mobile devices for flexibility in any setting.

---

### **Project Structure**

```bash
ShiftEase/
├── backend/         # Flask backend API
├── frontend/        # React frontend application
├── docs/            # Documentation
```

---

### **Prerequisites**

- Node.js (v16 or higher)
- Python (3.8 or higher)
- Firebase account
- Git

---

### **Quick Start**

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ShiftEase.git
    cd ShiftEase
    ```

2. **Set up the backend:**

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env     # Configure your environment variables
    ```

3. **Set up the frontend:**

    ```bash
    cd frontend
    npm install
    cp .env.example .env.local  # Configure your environment variables
    ```

4. **Start the development servers:**

    - **Backend:**

        ```bash
        cd backend
        python run.py
        ```

    - **Frontend:**

        ```bash
        cd frontend
        npm run dev
        ```

---

### **Documentation**

For detailed setup instructions and API documentation:

- [Backend Documentation]
- [Frontend Documentation]

---

### **License**

This project is licensed under the MIT License. See the LICENSE file for more details.
