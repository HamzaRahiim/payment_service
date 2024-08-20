from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from payment import setting
from payment.payment_pb2 import PaymentCreate

# Schema Registry configuration
schema_registry_conf = {'url': setting.SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    PaymentCreate, schema_registry_client, {'use.deprecated.format': False}
)

# Protobuf Deserializer
protobuf_deserializer = ProtobufDeserializer(
    PaymentCreate, {'use.deprecated.format': False}
)
