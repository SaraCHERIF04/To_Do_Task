import json
from http.server import BaseHTTPRequestHandler, HTTPServer

tasks = []

#hadi la  class will handle all incoming requests.
class RequestHandler(BaseHTTPRequestHandler):
    # read tasks
    def do_GET(self):
        
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode('utf-8'))

    def do_POST(self):
        # Add a new task
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data.decode('utf-8'))
            
            # Ensure we have required fields in the task data
            if 'title' not in task_data or 'description' not in task_data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Bad Request: Missing required fields'}).encode('utf-8'))
                return
            
            task_id = len(tasks) + 1
            task_data['id'] = task_id
            tasks.append(task_data)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Task created', 'task': task_data}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode('utf-8'))

    def do_PUT(self):
        # Update a task
        if self.path.startswith('/tasks/'):
            try:
                task_id = int(self.path.split('/')[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Bad Request: Invalid task ID'}).encode('utf-8'))
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data.decode('utf-8'))
            
            task_found = False
            for task in tasks:
                if task['id'] == task_id:
                    task.update(task_data)
                    task_found = True
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'Task updated', 'task': task}).encode('utf-8'))
                    break
            
            if not task_found:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Task not found'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode('utf-8'))

    def do_DELETE(self):
        # Delete a task
        if self.path.startswith('/tasks/'):
            try:
                task_id = int(self.path.split('/')[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Bad Request: Invalid task ID'}).encode('utf-8'))
                return

            task_found = False
            for i, task in enumerate(tasks):
                if task['id'] == task_id:
                    del tasks[i]
                    task_found = True
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'Task deleted'}).encode('utf-8'))
                    break
            
            if not task_found:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Task not found'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    """Starts the server and listens on the specified port"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
