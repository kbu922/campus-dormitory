<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>입사 신청</title>
</head>
<body>
    <h1>입사 신청</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color:green">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <form method="post">
        학번: <input type="text" name="student_id" required><br>
        이름: <input type="text" name="name" required><br>
        희망 호실(선택): <input type="text" name="room_number"><br>
        <button type="submit">입사 신청</button>
    </form>
</body>
</html>
