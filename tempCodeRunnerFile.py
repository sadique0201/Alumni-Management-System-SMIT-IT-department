user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # return redirect(url_for('home'), username=user)
            return render_template('index.html', username=user.username)
        flash('Invalid username or password')
    return render_template('login.html')