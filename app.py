from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)
load_dotenv()
# Database connection parameters
DB_HOST = "dpg-cq786rg8fa8c7386u0bg-a.singapore-postgres.render.com"
DB_NAME = "db1_rxhj"
DB_USER = "root"
DB_PASS = "cnQZRvsuSlaxtFk7QTlqZy1CCPRfvSkm"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    title = request.form['title']
    if video and title:
        # Save video to a file system or a cloud service here
        # Example: video.save(os.path.join('/path/to/save', video.filename))
        # Store video information in database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO videos (title, video_url) VALUES (%s, %s) RETURNING id;", (title, video.filename))
        vid_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Video uploaded successfully', 'video_id': vid_id})
    return jsonify({'message': 'Upload failed'}), 400

@app.route('/videos', methods=['GET'])
def fetch_videos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos;")
    videos = cursor.fetchall()
    cursor.close()
    return jsonify(videos)

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
