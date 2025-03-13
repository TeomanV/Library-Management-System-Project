from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models.book import Category, Author

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=13)])
    publisher = StringField('Publisher', validators=[Optional(), Length(max=100)])
    publication_year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=1800, max=2024)])
    edition = StringField('Edition', validators=[Optional(), Length(max=50)])
    description = TextAreaField('Description', validators=[Optional()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    location = StringField('Location', validators=[Optional(), Length(max=50)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Book')
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        self.author_id.choices = [(a.id, a.name) for a in Author.query.order_by(Author.name).all()]

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    search_by = SelectField('Search By', choices=[
        ('title', 'Title'),
        ('author', 'Author'),
        ('isbn', 'ISBN'),
        ('category', 'Category')
    ])
    submit = SubmitField('Search')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Category')

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    biography = TextAreaField('Biography', validators=[Optional()])
    birth_date = DateField('Birth Date', validators=[Optional()])
    death_date = DateField('Death Date', validators=[Optional()])
    submit = SubmitField('Save Author') 