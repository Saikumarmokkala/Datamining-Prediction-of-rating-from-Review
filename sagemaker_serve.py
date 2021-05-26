# This code is auto-generated.
import http.client as http_client
import logging
import os

import numpy as np
from joblib import load
from scipy import sparse

from sagemaker_containers.beta.framework import encoders
from sagemaker_containers.beta.framework import worker
from sagemaker_sklearn_extension.externals import read_csv_data


def _is_inverse_label_transform():
    """Returns True if if it's running in inverse label transform."""
    return os.getenv('AUTOML_TRANSFORM_MODE') == 'inverse-label-transform'


def _is_feature_transform():
    
    return os.getenv('AUTOML_TRANSFORM_MODE') == 'feature-transform'


def _sparsify_if_needed(x):
    
    if os.getenv('AUTOML_SPARSE_ENCODE_RECORDIO_PROTOBUF') == '1' \
            and not sparse.issparse(x):
        return sparse.csr_matrix(x)
    return x


def _split_features_target(x):
  
    if os.getenv('AUTOML_TRANSFORM_MODE') == 'feature-transform':
        return _sparsify_if_needed(x), None

    if sparse.issparse(x):
        return x[:, 1:], x[:, 0].toarray()
    return _sparsify_if_needed(x[:, 1:]), np.ravel(x[:, 0])


def model_fn(model_dir):
  
    return load(filename=os.path.join(model_dir, 'model.joblib'))


def predict_fn(input_object, model):
   
    if isinstance(input_object, worker.Response):
        return input_object

    if _is_inverse_label_transform():
        return model.inverse_label_transform(
            input_object.ravel().astype(np.float).astype(np.int)
        )
    try:
        return model.transform(input_object)
    except ValueError as e:
        return worker.Response(
            response='{}'.format(str(e) or 'Unknown error.'),
            status=http_client.BAD_REQUEST
        )


def input_fn(request_body, request_content_type):
   
    content_type = request_content_type.lower(
    ) if request_content_type else "text/csv"
    content_type = content_type.split(";")[0].strip()

    if content_type == 'text/csv':
        if isinstance(request_body, str):
            byte_buffer = request_body.encode()
        else:
            byte_buffer = request_body
        val = read_csv_data(source=byte_buffer)
        logging.info(f"Shape of the requested data: '{val.shape}'")
        return val

    return worker.Response(
        response=f"'{request_content_type}' is an unsupported content type.",
        status=http_client.UNSUPPORTED_MEDIA_TYPE
    )


def output_fn(prediction, accept_type):
    
    if isinstance(prediction, worker.Response):
        return prediction

    if _is_inverse_label_transform():
        if accept_type == 'text/csv':
            return worker.Response(
                response=encoders.encode(prediction, accept_type),
                status=http_client.OK,
                mimetype=accept_type
            )
        else:
            return worker.Response(
                response=f"Accept type '{accept_type}' is not supported "
                         f"during inverse label transformation.",
                status=413
            )

    if isinstance(prediction, tuple):
        X, y = prediction
    else:
        X, y = _split_features_target(prediction)

    if accept_type == 'application/x-recordio-protobuf':
        return worker.Response(
            response=encoders.array_to_recordio_protobuf(
                _sparsify_if_needed(X).astype('float32'),
                y.astype('float32') if y is not None else y
            ),
            status=http_client.OK,
            mimetype=accept_type
        )

    if accept_type == 'text/csv':
        if y is not None:
            X = np.column_stack(
                (np.ravel(y), X.todense() if sparse.issparse(X) else X)
            )

        return worker.Response(
            response=encoders.encode(X, accept_type),
            status=http_client.OK,
            mimetype=accept_type
        )
    return worker.Response(
        response=f"Accept type '{accept_type}' is not supported.",
        status=http_client.NOT_ACCEPTABLE
    )


def execution_parameters_fn():
    
    if _is_feature_transform():
        return worker.Response(
            response='{"MaxPayloadInMB":1}',
            status=http_client.OK,
            mimetype="application/json"
        )
    return worker.Response(
        response='{"MaxPayloadInMB":6}',
        status=http_client.OK,
        mimetype="application/json"
    )
