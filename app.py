from flask import Flask, render_template, request, redirect, flash, session, Response
from flask_mail import Mail, Message
import mysql.connector
import csv
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',
    MAIL_PASSWORD='your_app_password'
)
mail = Mail(app)

# ✅ DB 연결 함수
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ✅ 사용 가능한 방 자동 배정 함수
def assign_available_room(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT room_number 
        FROM all_rooms 
        WHERE room_number NOT IN (SELECT room_number FROM rooms)
        LIMIT 1
    """)
    row = cur.fetchone()
    return row[0] if row else None

# ✅ 메일 알림 함수
def send_notification(email, subject, body):
    msg = Message(subject, recipients=[email], body=body, sender='your_email@gmail.com')
    mail.send(msg)

# ✅ 홈
@app.route('/')
def home():
    return '''
        <h1>기숙사 입퇴사 시스템입니다.</h1>
        <ul>
            <li><a href="/checkin">입사 신청</a></li>
            <li><a href="/checkout">퇴사 신청</a></li>
            <li><a href="/admin">관리자 페이지</a></li>
        </ul>
    '''

# ✅ 입사 신청
@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        room_number = request.form.get('room_number')

        conn = get_db()
        cur = conn.cursor()

        if not room_number:
            room_number = assign_available_room(conn)

        cur.execute("""
            INSERT INTO checkin_requests (student_id, name, preferred_room) 
            VALUES (%s, %s, %s)
        """, (student_id, name, room_number))
        conn.commit()
        cur.close()
        conn.close()

        flash('입사 신청이 접수되었습니다. 관리자의 승인을 기다려주세요.')
        return redirect('/checkin')

    return render_template('checkin.html')

# ✅ 퇴사 신청
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        student_id = request.form['student_id']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT room_number FROM rooms WHERE student_id = %s", (student_id,))
        row = cur.fetchone()

        if not row:
            flash('입사 기록이 없습니다.')
            return redirect('/checkout')

        room_number = row[0]
        cur.execute("DELETE FROM rooms WHERE room_number = %s", (room_number,))
        cur.execute("""
            INSERT INTO checkin_out (student_id, room_number, status) 
            VALUES (%s, %s, '퇴사')
        """, (student_id, room_number))
        conn.commit()
        cur.close()
        conn.close()

        flash('퇴사 신청이 완료되었습니다.')
        return redirect('/checkout')

    return render_template('checkout.html')

# ✅ 관리자 학생 조회 페이지
@app.route('/admin')
def admin_page():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.student_id, s.name, r.room_number 
        FROM students s 
        LEFT JOIN rooms r ON s.student_id = r.student_id
    """)
    students = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin.html', students=students)

# ✅ 관리자 요청 확인 페이지
@app.route('/admin/requests')
def view_requests():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM checkin_requests WHERE status='대기'")
    requests = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_requests.html', requests=requests)

# ✅ 입사 승인
@app.route('/admin/approve/<int:req_id>')
def approve_request(req_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM checkin_requests WHERE id=%s", (req_id,))
    req = cur.fetchone()

    if not req:
        flash("요청을 찾을 수 없습니다.")
        return redirect('/admin/requests')

    cur.execute("INSERT IGNORE INTO students (student_id, name) VALUES (%s, %s)", (req['student_id'], req['name']))
    cur.execute("INSERT INTO rooms (room_number, student_id) VALUES (%s, %s)", (req['preferred_room'], req['student_id']))
    cur.execute("INSERT INTO checkin_out (student_id, room_number, status) VALUES (%s, %s, '입사')", (req['student_id'], req['preferred_room']))
    cur.execute("UPDATE checkin_requests SET status='승인' WHERE id=%s", (req_id,))
    conn.commit()
    cur.close()
    conn.close()

    flash("입사 요청이 승인되었습니다.")
    return redirect('/admin/requests')

# ✅ CSV 다운로드
@app.route('/admin/download')
def download_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM checkin_out")
    rows = cur.fetchall()
    headers = [i[0] for i in cur.description]

    def generate():
        yield ','.join(headers) + '\n'
        for row in rows:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=checkin_out_records.csv"})

# ✅ 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
