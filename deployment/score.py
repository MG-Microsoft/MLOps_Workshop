import json
import numpy
import joblib
import time
from azureml.core.model import Model

# from inference_schema.schema_decorators \
#     import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type \
#     import NumpyParameterType


def init():
    global LGBM_MODEL
    # Load the model from file into a global object
    model_path = Model.get_model_path("insurance_model.pkl")
    LGBM_MODEL = joblib.load(model_path)
    # Print statement for appinsights custom traces:
    print("model initialized" + time.strftime("%H:%M:%S"))


# Inference_schema generates a schema for your web service
# It then creates an OpenAPI (Swagger) specification for the web service
# at http://<scoring_base_url>/swagger.json
# @input_schema('raw_data', NumpyParameterType(input_sample))
# @output_schema(NumpyParameterType(output_sample))
def run(raw_data, request_headers):
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    result = LGBM_MODEL.predict(data)
    # Log the input and output data to appinsights:
    info = {
        "input": raw_data,
        "output": result.tolist()
        }
    print(json.dumps(info))
    # Demonstrate how we can log custom data into the Application Insights
    # traces collection.
    # The 'X-Ms-Request-id' value is generated internally and can be used to
    # correlate a log entry with the Application Insights requests collection.
    # The HTTP 'traceparent' header may be set by the caller to implement
    # distributed tracing (per the W3C Trace Context proposed specification)
    # and can be used to correlate the request to external systems.
    print(('{{"RequestId":"{0}", '
           '"TraceParent":"{1}", '
           '"NumberOfPredictions":{2}}}'
           ).format(
               request_headers.get("X-Ms-Request-Id", ""),
               request_headers.get("Traceparent", ""),
               len(result)
    ))

    return {"result": result.tolist()}
