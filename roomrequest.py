<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>입사 요청 목록</title>
</head>
<body>
    <h1>입사 요청 목록</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color:blue">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <table border="1">
        <tr>
            <th>요청 ID</th>
            <th>학번</th>
            <th>이름</th>
            <th>희망 호실</th>
            <th>상태</th>
            <th>승인</th>
        </tr>
        {% for req in requests %}
        <tr>
            <td>{{ req.id }}</td>
            <td>{{ req.student_id }}</td>
            <td>{{ req.name }}</td>
            <td>{{ req.preferred_room or '없음' }}</td>
            <td>{{ req.status }}</td>
            <td><a href="/admin/approve/{{ req.id }}">승인</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
