from core.models.people_counter import PeopleCounter


class PeopleCounterSerializer:
    model = PeopleCounter

    @classmethod
    def to_model(cls, data):
        try:
            model_data = {
                "name": data["name"], "in_": int(data["in"]), "out": int(data["out"]),
                "ts": data["ts"]
            }
            return cls.model(**model_data)
        except KeyError as exc:
            raise ValidationError(f'Missing required information: {exc}')
        except TypeError:
            raise ValidationError(f'Out and/or In are not valid')


class ValidationError(ValueError):
    pass
