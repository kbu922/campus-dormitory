<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>관리자 페이지</title>
</head>
<body>
    <h1>학생 목록</h1>
    <table border="1">
        <tr>
            <th>학번</th>
            <th>이름</th>
            <th>호실</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student.student_id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.room_number or '배정 안됨' }}</td>
        </tr>
        {% endfor %}
    </table>

    <br>
    <a href="/admin/requests">입사 요청 목록 보기</a> |
    <a href="/admin/download">CSV 다운로드</a>
</body>
</html>
