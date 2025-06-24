<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>퇴사 신청</title>
</head>
<body>
    <h1>퇴사 신청</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color:red">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <form method="post">
        학번: <input type="text" name="student_id" required><br>
        <button type="submit">퇴사 신청</button>
    </form>
</body>
</html>
