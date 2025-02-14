# vivea_health/schema.py
import graphene
import jwt

# Ensure you use the same secret key as in jwt_helpers.py
SECRET_KEY = 'your-secret-key'

# Define the Patient type with desired fields
class Patient(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()
    conditions = graphene.List(graphene.String)
    last_appointment = graphene.String()
    ai_summary = graphene.String()

# Define your Query class and include token validation in resolvers
class Query(graphene.ObjectType):
    patient = graphene.Field(Patient, id=graphene.ID(required=True))

    def resolve_patient(self, info, id):
        # Access the Flask request from the context
        auth_header = info.context.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except Exception as e:
                raise Exception("Unauthorized: " + str(e))
        else:
            raise Exception("Missing Authorization header")
        
        # Replace the following with real data from your FHIR API or manual inputs
        sample_patient = {
            "id": id,
            "name": "John Doe",
            "age": 45,
            "conditions": ["Hypertension", "Diabetes"],
            "last_appointment": "2025-01-15",
            "ai_summary": "Patient shows stable vitals with moderate risk factors."
        }
        return Patient(**sample_patient)

schema = graphene.Schema(query=Query)
