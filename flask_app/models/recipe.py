from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app import DATABASE, bcrypt
from flask import session, flash


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.time = data['time']
        self.instructions = data['instructions']
        self.datemade = data['datemade']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,form):

        data = {
            **form,
            "users_id" : session['user_id']
        }

        query = """
            INSERT INTO recipes (title, description, time, instructions, datemade, users_id) 
            VALUES (%(title)s,%(description)s,%(time)s, %(instructions)s, %(datemade)s, %(users_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all_recipes(cls):

        query = """
                SELECT * FROM recipes
                LEFT JOIN users ON recipes.users_id = users.id;
                """
        results = connectToMySQL(DATABASE).query_db(query)

        recipe_list = []
        
        if results:
            for row in results:
                food = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                food.creator = User(user_data)

                recipe_list.append(food)
                print(recipe_list)
        return recipe_list


    @classmethod
    def get_one(cls,id):
        data = {
        "id" : id
        }

        query  = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def get_name(cls,data):
        query  = "SELECT * FROM user WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def save_recipe(cls, data):
        query = """
            UPDATE recipes 
            SET title = %(title)s, 
            description = %(description)s, 
            instructions = %(instructions)s, 
            datemade = %(datemade)s, 
            time = %(time)s
            WHERE id = %(id)s;
            """
        
        result = connectToMySQL(DATABASE).query_db( query, data )
        print(result)
        return result

    @classmethod
    def destroy(cls, id):
        data = {
            'id' : id
        }
        query = """DELETE FROM recipes 
        WHERE recipes.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def validate_recipe(cls, form):
        print(form)
        is_valid = True

        if len(form['title']) < 3:
            is_valid= False
            flash("Recipe name must be at least 3 characters", 'rerror')
        if len(form['description']) < 5:
            is_valid= False
            flash("Please write a description", 'rerror')
        if len(form['instructions']) < 8:
            is_valid= False
            flash("Instructions must be included ", 'rerror')
        if len(form['datemade']) < 8:
            is_valid= False
            flash("Date when recipe was made", 'rerror')
        if not 'time' in form:
            is_valid= False
            flash("Was it under 30 minutes?", 'rerror')
        return is_valid

    @classmethod
    def get_one_by_id(cls,id):
        data = {
            "id" : id
        }
        query = '''
                SELECT * FROM recipes
                JOIN users ON users_id = users.id
                WHERE recipes.id = %(id)s;
                '''
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            row = results[0]
            one_recipe = cls(row)
            user_data = {
                **row,
                "id" : row['users.id'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            one_recipe.creator = User(user_data)
            return one_recipe