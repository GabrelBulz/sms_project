from sqlalchemy.orm import sessionmaker


def add_obj(engine):
    Session = sessionmaker(bind=engine)

    session = Session()

    user=user()
    user.id=sadsad


    session.add(user)
    session.commit()
    session.close()