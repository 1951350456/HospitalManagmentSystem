# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'HospitalManagement',
    'charset': 'utf8mb4'

}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG,cursorclass=pymysql.cursors.DictCursor)

# 登录限制装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 这里简化为明文存储，生产环境应使用哈希
        conn = get_db_connection()
        cursor = conn.cursor()
        # 检查用户名是否存在
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            flash('用户名已存在')
            cursor.close()
            conn.close()
            return render_template('register.html')
        # 插入新用户
        cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    return render_template('register.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('index'))
        flash('用户名或密码错误')
    return render_template('login.html')

# 退出登录
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# 首页
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# 错误网页
# 这是关键部分：定义404错误处理器
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
# ------------------------------------------------
# 以下为各模块示例路由及功能，需根据实际需求补充完善
# ------------------------------------------------

# 药品类型管理
@app.route('/medicine_types')
@login_required
def medicine_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 类型ID, 类型名称, 描述 FROM 药品类型")
    types = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicine_types.html', types=types)

@app.route('/medicine_types/add', methods=['GET', 'POST'])
@login_required
def add_medicine_type():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO 药品类型(类型名称, 描述) VALUES(%s, %s)", (name, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('medicine_types'))
    return render_template('add_medicine_type.html')

# 药品信息管理
@app.route('/medicines')
@login_required
def medicines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT y.药品ID, y.药品名称, l.类型名称, y.规格, y.单位, y.生产厂家, y.价格, y.库存量 FROM 药品信息 y JOIN 药品类型 l ON y.类型ID=l.类型ID")
    medicines = cursor.fetchall()
    cursor.execute("SELECT * FROM 药品库存视图")
    total_stocks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicines.html', medicines=medicines, total_stocks=total_stocks)

@app.route('/medicines/add', methods=['GET', 'POST'])
@login_required
def add_medicine():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        spec = request.form['spec']
        unit = request.form['unit']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        conn_insert = get_db_connection()
        cursor_insert = conn_insert.cursor()
        cursor_insert.execute("INSERT INTO 药品信息(药品名称, 类型ID, 规格, 单位, 生产厂家, 价格) VALUES(%s, %s, %s, %s, %s, %s)",
                              (name, type_id, spec, unit, manufacturer, price))
        conn_insert.commit()
        cursor_insert.close()
        conn_insert.close()
        return redirect(url_for('medicines'))
    cursor.execute("SELECT 类型ID, 类型名称 FROM 药品类型")
    types = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_medicine.html', types=types)

# 科室管理
@app.route('/departments')
@login_required
def departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 科室ID, 科室名称, 负责人, 描述 FROM 科室")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('departments.html', departments=departments)

@app.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        leader = request.form['leader']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO 科室(科室名称, 负责人, 描述) VALUES(%s, %s, %s)",
                       (name, leader, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('departments'))
    return render_template('add_department.html')

# 医生管理
@app.route('/doctors')
@login_required
def doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT d.医生ID, d.姓名, d.性别, d.职称, k.科室名称, d.联系电话, d.入职日期 FROM 医生 d LEFT JOIN 科室 k ON d.所属科室ID=k.科室ID")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        title = request.form['title']
        department_id = request.form['department_id']
        phone = request.form['phone']
        hire_date = request.form['hire_date']
        cursor.execute("INSERT INTO 医生(姓名, 性别, 职称, 所属科室ID, 联系电话, 入职日期) VALUES(%s, %s, %s, %s, %s, %s)",
                       (name, gender, title, department_id, phone, hire_date))
        conn.commit()
        return redirect(url_for('doctors'))
    cursor.execute("SELECT 科室ID, 科室名称 FROM 科室")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_doctor.html', departments=departments)

# 病人管理
@app.route('/patients')
@login_required
def patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 病人ID, 姓名, 性别, 出生日期, 联系电话, 住址, 医保卡号 FROM 病人")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']
        card_number = request.form['card_number']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO 病人(姓名, 性别, 出生日期, 联系电话, 住址, 医保卡号) VALUES(%s, %s, %s, %s, %s, %s)",
                       (name, gender, birth_date, phone, address, card_number))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

# 处方登记
@app.route('/prescriptions', methods=['GET', 'POST'])
@login_required
def prescriptions():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        cursor.execute("INSERT INTO 处方(病人ID, 医生ID, 诊断结果) VALUES(%s, %s, %s)",
                       (patient_id, doctor_id, diagnosis))
        conn.commit()
        return redirect(url_for('prescriptions'))
    cursor.execute("SELECT p.处方ID, b.姓名 as 病人姓名, d.姓名 as 医生姓名, p.诊断结果, p.开具时间 FROM 处方 p JOIN 病人 b ON p.病人ID=b.病人ID JOIN 医生 d ON p.医生ID=d.医生ID ORDER BY p.开具时间 DESC")
    prescriptions = cursor.fetchall()
    cursor.execute("SELECT 病人ID, 姓名 FROM 病人")
    patients = cursor.fetchall()
    cursor.execute("SELECT 医生ID, 姓名, 科室名称 FROM 医生 JOIN 科室 ON 医生.所属科室ID=科室.科室ID")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('prescriptions.html', prescriptions=prescriptions, patients=patients, doctors=doctors)


# 处方明细添加
@app.route('/prescription/<int:prescription_id>/details', methods=['GET', 'POST'])
@login_required
def prescription_details(prescription_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        usage = request.form['usage']
        cursor.execute("INSERT INTO 处方明细(处方ID, 药品ID, 数量, 用法用量) VALUES(%s, %s, %s, %s)",
                       (prescription_id, medicine_id, quantity, usage))
        conn.commit()
        return redirect(url_for('prescription_details', prescription_id=prescription_id))
    cursor.execute("SELECT m.明细ID, y.药品名称, m.数量, m.用法用量 FROM 处方明细 m JOIN 药品信息 y ON m.药品ID=y.药品ID WHERE m.处方ID=%s", (prescription_id,))
    details = cursor.fetchall()
    cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
    medicines = cursor.fetchall()
    cursor.execute("SELECT 处方ID, b.姓名 AS 病人, d.姓名 AS 医生, p.开具时间, p.诊断结果 FROM 处方 p JOIN 病人 b ON p.病人ID=b.病人ID JOIN 医生 d ON p.医生ID=d.医生ID WHERE p.处方ID=%s", (prescription_id,))
    prescription_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('prescription_details.html', details=details, medicines=medicines, prescription=prescription_info)

# 收费管理
@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        prescription_id = request.form['prescription_id']

        cashier = session.get('username')
        date = request.form['datetime']
        payment_method = request.form['payment_method']
        cursor.execute("SELECT * FROM 未缴费处方 WHERE 处方ID=%s",(prescription_id,))
        amount = cursor.fetchone()['待缴费金额']
        cursor.execute("INSERT INTO 收费记录(处方ID, 收费金额, 收费时间, 收费员, 支付方式) VALUES(%s, %s, %s, %s, %s)",
                       (prescription_id, amount, date, cashier, payment_method))
        conn.commit()
        return redirect(url_for('billing'))
    cursor.execute("SELECT b.收费ID, p.处方ID, b.收费金额, b.收费时间, b.收费员, b.支付方式, t.姓名 as 病人姓名 FROM 收费记录 b JOIN 处方 p ON b.处方ID=p.处方ID JOIN 病人 t ON p.病人ID=t.病人ID ORDER BY b.收费时间 DESC")
    bills = cursor.fetchall()
    cursor.execute("SELECT p.处方ID, t.姓名 as 病人姓名, d.姓名 as 医生姓名, p.开具时间, p.诊断结果 FROM 处方 p JOIN 病人 t ON p.病人ID=t.病人ID JOIN 医生 d ON p.医生ID=d.医生ID")
    prescriptions_list = cursor.fetchall()
    cursor.execute("SELECT * FROM 未缴费处方")
    unpaid_pres = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('billing.html', bills=bills, prescriptions=prescriptions_list, unpaid_pres=unpaid_pres)

# 药品入库 （自动更新库存由触发器完成）
@app.route('/stock_in', methods=['GET', 'POST'])
@login_required
def stock_in():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        date = request.form['datetime']
        operator = session.get('username')
        supplier = request.form['supplier']
        cursor.execute("INSERT INTO 入库记录(药品ID, 数量, 入库时间, 操作员, 供应商) VALUES(%s, %s, %s, %s, %s)",
                       (medicine_id, quantity, date, operator, supplier))
        conn.commit()
        return redirect(url_for('stock_in'))
    cursor.execute("SELECT s.入库ID, m.药品名称, s.数量, s.入库时间, s.操作员, s.供应商 FROM 入库记录 s JOIN 药品信息 m ON s.药品ID=m.药品ID ORDER BY s.入库时间 DESC")
    stock_ins = cursor.fetchall()
    cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stock_in.html', stock_ins=stock_ins, medicines=medicines)

# 药品出库 （自动更新库存由触发器完成）
@app.route('/stock_out', methods=['GET', 'POST'])
@login_required
def stock_out():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        date = request.form['datetime']
        operator = session.get('username')
        departments = request.form['departments']
        try:
            cursor.execute("INSERT INTO 出库记录(药品ID, 数量, 出库时间, 操作员, 领用科室) VALUES(%s, %s, %s, %s, %s)",
                           (medicine_id, quantity, date, operator, departments))
            conn.commit()
        except Exception as e:
            conn.rollback()
            error_message = '出库数量超过库存数量'
            flash('<span class="error-message">出库数量超过库存数量</span>')
        return redirect(url_for('stock_out'))
    cursor.execute("SELECT s.出库ID, m.药品名称, s.数量, s.出库时间, s.操作员, s.领用科室 FROM 出库记录 s JOIN 药品信息 m ON s.药品ID=m.药品ID ORDER BY s.出库时间 DESC")
    stock_outs = cursor.fetchall()
    cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
    medicines = cursor.fetchall()
    cursor.execute("SELECT 科室ID, 科室名称 FROM 科室")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stock_out.html', stock_outs=stock_outs, medicines=medicines, departments=departments)



# 数据备份（导出 SQL 文件）
@app.route('/backup')
@login_required
def backup():
    # 这里示例简化，不做真正的备份，仅提示
    flash('备份功能需要在服务器环境中使用 mysqldump 等工具实现')
    return redirect(url_for('index'))

# 数据恢复提示
@app.route('/restore')
@login_required
def restore():
    flash('恢复功能请使用 MySQL 客户端或命令行工具执行 SQL 文件导入')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


# --------------------------------------------
# 以下为对应的 HTML 模板示例，存放在 templates/ 文件夹中
# --------------------------------------------
# templates/base.html
"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>医院信息管理系统</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/css/bootstrap.min.css">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">医院管理</a>
  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item"><a class="nav-link" href="{{ url_for('index') }}">首页</a></li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="medicineMenu" data-toggle="dropdown">药品管理</a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="{{ url_for('medicine_types') }}">药品类型</a>
          <a class="dropdown-item" href="{{ url_for('medicines') }}">药品信息</a>
          <a class="dropdown-item" href="{{ url_for('stock_in') }}">药品入库</a>
          <a class="dropdown-item" href="{{ url_for('stock_out') }}">药品出库</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="personnelMenu" data-toggle="dropdown">人员管理</a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="{{ url_for('departments') }}">科室管理</a>
          <a class="dropdown-item" href="{{ url_for('doctors') }}">医生管理</a>
          <a class="dropdown-item" href="{{ url_for('patients') }}">病人管理</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="businessMenu" data-toggle="dropdown">业务管理</a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="{{ url_for('prescriptions') }}">处方登记</a>
          <a class="dropdown-item" href="{{ url_for('billing') }}">收费管理</a>
        </div>
      </li>
      <li class="nav-item"><a class="nav-link" href="{{ url_for('backup') }}">数据备份</a></li>
      <li class="nav-item"><a class="nav-link" href="{{ url_for('restore') }}">数据恢复</a></li>
    </ul>
    <ul class="navbar-nav ml-auto">
      {% if session.username %}
      <li class="nav-item"><a class="nav-link" href="#">{{ session.username }}</a></li>
      <li class="nav-item"><a class="nav-link" href="{{ url_for('logout') }}">退出</a></li>
      {% else %}
      <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">登录</a></li>
      <li class="nav-item"><a class="nav-link" href="{{ url_for('register') }}">注册</a></li>
      {% endif %}
    </ul>
  </div>
</nav>
<div class="container mt-4">
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for msg in messages %}
          <div class="alert alert-warning">{{ msg }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
</div>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# templates/register.html
"""
{% extends 'base.html' %}
{% block content %}
<h2>注册</h2>
<form method="post">
  <div class="form-group">
    <label>用户名：</label>
    <input type="text" name="username" class="form-control" required>
  </div>
  <div class="form-group">
    <label>密码：</label>
    <input type="password" name="password" class="form-control" required>
  </div>
  <button type="submit" class="btn btn-primary">注册</button>
</form>
{% endblock %}
"""

# templates/login.html
"""
{% extends 'base.html' %}
{% block content %}
<h2>登录</h2>
<form method="post">
  <div class="form-group">
    <label>用户名：</label>
    <input type="text" name="username" class="form-control" required>
  </div>
  <div class="form-group">
    <label>密码：</label>
    <input type="password" name="password" class="form-control" required>
  </div>
  <button type="submit" class="btn btn-primary">登录</button>
</form>
{% endblock %}
"""

# templates/index.html
"""
{% extends 'base.html' %}
{% block content %}
<h1>欢迎来到医院信息管理系统</h1>
<p>请选择左侧或上方菜单进行操作。</p>
{% endblock %}
"""

# 以下模板文件结构与示例（同理可创建增删改查页面）：
# medicine_types.html, add_medicine_type.html, medicines.html, add_medicine.html
# stock_in.html, stock_out.html
# departments.html, add_department.html
# doctors.html, add_doctor.html
# patients.html, add_patient.html
# prescriptions.html, prescription_details.html
# billing.html

# 例如：templates/medicine_types.html
"""
{% extends 'base.html' %}
{% block content %}
<h2>药品类型列表</h2>
<a href="{{ url_for('add_medicine_type') }}" class="btn btn-success mb-2">添加类型</a>
<table class="table table-bordered">
  <thead>
    <tr><th>ID</th><th>名称</th><th>描述</th></tr>
  </thead>
  <tbody>
    {% for t in types %}
    <tr>
      <td>{{ t[0] }}</td>
      <td>{{ t[1] }}</td>
      <td>{{ t[2] }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
"""

# 其他模板可参照以上风格，根据路由传入的数据进行渲染。
