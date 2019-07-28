1. How long did you spend on the coding test below? What would you add to your solution if you had more time? If you didn't spend much time on the coding test then use this as an opportunity to explain what you would add.

I spent one week to develop the project if I had time I will add a search filter feature, and I will use Vue JS  for front end 


2. What was the most useful feature that was added to the latest version of your chosen language? Please include a snippet of code that shows how you've used it.


 What was the most useful feature that was added to the latest version of your chosen language? Please include a snippet of code that shows how you've used it.

 this part of my code 

    from favoriteThings.users.routes import users
    from favoriteThings.favorites.routes import favorites
    from favoriteThings.categories.routes import categories
    from favoriteThings.logs.routes import logs
    from favoriteThings.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(favorites)
    app.register_blueprint(categories)
    app.register_blueprint(main)
    app.register_blueprint(logs)

3.How would you track down a performance issue in production? Have you ever had to do this
when I face a problem, first I read the error then search the line of error, then search the reason of error using google or print  command until solve it 
