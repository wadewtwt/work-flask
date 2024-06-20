from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# 配置MySQL数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:940327Wt!@139.224.60.242:3306/some-note'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 定义数据库模型
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}')"


# 创建数据库（如果不存在）
@app.before_first_request
def create_tables():
    db.create_all()


# 路由和视图函数
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data.get('name') or not data.get('description'):
        return jsonify({'message': 'Missing name or description'}), 400

    new_item = Item(name=data['name'], description=data['description'])
    try:
        db.session.add(new_item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Item already exists'}), 409
    return jsonify({'message': 'Item added successfully'}), 201


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])


@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    if data.get('name'):
        item.name = data['name']
    if data.get('description'):
        item.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)