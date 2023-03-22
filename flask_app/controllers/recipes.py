from flask_app import app
from flask import render_template,session,flash,redirect, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipe/new')
def add_new():

    if 'user_id' not in session:
        return redirect('/')

    return render_template("/new.html")


@app.route('/recipe/save',methods=['POST'])
def saverecipe():

    if 'user_id' not in session:
        return redirect('/')

    completed = Recipe.validate_recipe(request.form)
    
    if not completed:
        return redirect('/recipe/new')

    Recipe.save(request.form)
    return redirect('/dashboard')


@app.route('/recipecard/<int:id>')
def displayrecipe(id):

    if 'user_id' not in session:
        return redirect('/')


    recipe_info = Recipe.get_one_by_id(id)
    return render_template("/recipecard.html", info = recipe_info)


@app.route('/recipes/edit/<int:id>')
def edit(id):

    if 'user_id' not in session:
        return redirect('/')

    return render_template("/edit.html", user=User.get_one_by_id(session['user_id']), recipe=Recipe.get_one_by_id(id))

@app.route('/recipes/update',methods=['POST'])
def recipes_update():

    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')

    print(request.form)
    Recipe.save_recipe(request.form)

    return redirect('/dashboard')



@app.route('/recipes/destroy/<int:id>')
def destroy(id):
    
    if 'user_id' not in session:
        return redirect('/')

    Recipe.destroy(id)
    return redirect('/dashboard')