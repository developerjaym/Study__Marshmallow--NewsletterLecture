#!/usr/bin/env python3

from faker import Faker

from app import app
from models import db, Newsletter, Writer, Tag

with app.app_context():
    
    fake = Faker()

    Writer.query.delete()
    Tag.query.delete()
    Newsletter.query.delete()

    tags_to_save = ["Local", "Weather", "Crime", "Florida"]
    
    newsletters = []
    for i in range(50):
        writer = Writer(name=fake.name())
        db.session.add(writer)
        db.session.flush()
        print(writer.id)
        newsletter = Newsletter(
            title = fake.text(max_nb_chars=20),
            body = fake.paragraph(nb_sentences=5),
            writer_id = writer.id
        )
        db.session.add(newsletter)
        db.session.flush()
        for tag_to_save in tags_to_save:
            tag = Tag(content=tag_to_save, newsletter_id=newsletter.id)
            tag = db.session.add(tag)
    db.session.commit()



