from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_PATH = 'items.json'

# --- Funcții pentru încărcare și salvare JSON ---
def load_data():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Rute API ---
@app.route('/')
def index():
    # Pagina HTML cu JS inline
    return render_template_string("""
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Catalog Cărți</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-4">
<div class="container">
    <h1>Catalog de Cărți</h1>
    <div id="message"></div>
    <table class="table table-bordered" id="booksTable">
        <thead>
            <tr><th>ID</th><th>Titlu</th><th>Autor</th><th>Acțiuni</th></tr>
        </thead>
        <tbody></tbody>
    </table>
    <h3 id="formTitle">Adaugă carte</h3>
    <form id="bookForm">
        <input type="hidden" id="bookId">
        <div class="mb-2">
            <input type="text" id="title" placeholder="Titlu" class="form-control" required>
        </div>
        <div class="mb-2">
            <input type="text" id="author" placeholder="Autor" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success">Salvează</button>
        <button type="button" id="cancelEdit" class="btn btn-secondary" style="display:none;">Anulează</button>
    </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', loadBooks);
const form = document.getElementById('bookForm');
const messageDiv = document.getElementById('message');
const cancelEditBtn = document.getElementById('cancelEdit');

form.addEventListener('submit', handleFormSubmit);
cancelEditBtn.addEventListener('click', resetForm);

function showMessage(msg, type='success') {
    messageDiv.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
    setTimeout(() => messageDiv.innerHTML = '', 2000);
}

function loadBooks() {
    fetch('/items')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#booksTable tbody');
            tbody.innerHTML = '';
            data.forEach(book => {
                tbody.innerHTML += `
                    <tr>
                        <td>${book.id}</td>
                        <td>${book.title}</td>
                        <td>${book.author}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" onclick="editBook(${book.id})">Edit</button>
                            <button class="btn btn-danger btn-sm" onclick="deleteBook(${book.id})">Delete</button>
                        </td>
                    </tr>`;
            });
        });
}

function editBook(id) {
    fetch(`/items/${id}`)
        .then(res => {
            if (!res.ok) throw new Error('Carte negăsită');
            return res.json();
        })
        .then(book => {
            document.getElementById('bookId').value = book.id;
            document.getElementById('title').value = book.title;
            document.getElementById('author').value = book.author;
            document.getElementById('formTitle').innerText = 'Editează carte';
            cancelEditBtn.style.display = 'inline-block';
        })
        .catch(e => showMessage(e.message, 'danger'));
}

function deleteBook(id) {
    if (!confirm('Sigur ștergi această carte?')) return;
    fetch(`/items/${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            if (data.message) showMessage(data.message, 'success');
            else showMessage(data.error, 'danger');
            loadBooks();
        });
}

function handleFormSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('bookId').value;
    const title = document.getElementById('title').value.trim();
    const author = document.getElementById('author').value.trim();
    if (!title || !author) {
        showMessage('Completează toate câmpurile!', 'danger');
        return;
    }
    const payload = { title, author };
    if (id) {
        fetch(`/items/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) showMessage(data.error, 'danger');
            else showMessage('Carte actualizată!');
            resetForm();
            loadBooks();
        });
    } else {
        fetch('/items', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) showMessage(data.error, 'danger');
            else showMessage('Carte adăugată!');
            resetForm();
            loadBooks();
        });
    }
}

function resetForm() {
    form.reset();
    document.getElementById('bookId').value = '';
    document.getElementById('formTitle').innerText = 'Adaugă carte';
    cancelEditBtn.style.display = 'none';
}
</script>
</body>
</html>
    """)

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(load_data()), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = load_data()
    for item in items:
        if item['id'] == item_id:
            return jsonify(item), 200
    return jsonify({'error': 'Not found'}), 404

@app.route('/items', methods=['POST'])
def create_item():
    items = load_data()
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    new_id = max([item['id'] for item in items], default=0) + 1
    new_item = {'id': new_id, 'title': data['title'], 'author': data['author']}
    items.append(new_item)
    save_data(items)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    items = load_data()
    data = request.get_json()
    for item in items:
        if item['id'] == item_id:
            item['title'] = data.get('title', item['title'])
            item['author'] = data.get('author', item['author'])
            save_data(items)
            return jsonify(item), 200
    return jsonify({'error': 'Not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()
    for i, item in enumerate(items):
        if item['id'] == item_id:
            items.pop(i)
            save_data(items)
            return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    # Dacă nu există fișierul JSON, creează unul de test cu 3 cărți
    if not os.path.exists(DATA_PATH):
        sample = [
            {"id": 1, "title": "1984", "author": "George Orwell"},
            {"id": 2, "title": "Enigma Otiliei", "author": "George Călinescu"},
            {"id": 3, "title": "Ion", "author": "Liviu Rebreanu"}
        ]
        save_data(sample)
    app.run(debug=True)
