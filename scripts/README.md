# 🛠️ Python Quick Solutions

This is my starting point for building Python scripts that turn ideas into practical solutions — fast, simple, and useful.

This repo is meant to grow into a collection of small, focused Python tools that automate tasks, explore data, and solve real-world problems with minimal setup.

## 📋 Current Tool

### `server_check.py`

A lightweight script to remotely check the health of a Linux or macOS server over SSH.

#### 🔍 Features
- SSH into a remote server using a password or key
- Automatically detects OS type (Linux or macOS)
- Runs OS-specific system health commands
- Logs all output to a timestamped file in the `logs/` directory

#### ⚙️ Example Usage

```bash
python scripts/server_check.py 192.168.1.100 -u bob -p

---

## 🗂️ Folder Structure

python-quick-solutions/ ├── scripts/ │ └── server_check.py ├── logs/ │ └── (auto-generated log files) ├── venv/ (not tracked) └── README.md

---

## ✅ Next Steps

- [ ] Add more troubleshooting or automation scripts
- [ ] Refactor common logic into `utils.py`
- [ ] Add multi-host support (run checks on a list of servers)

