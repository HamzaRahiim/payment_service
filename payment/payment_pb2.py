# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpayment.proto\"\xaa\x01\n\rPaymentCreate\x12\x12\n\ncreated_at\x18\x01 \x01(\x03\x12\x10\n\x08\x63\x61rd_num\x18\x02 \x01(\x03\x12\x0b\n\x03\x63vv\x18\x03 \x01(\x05\x12\x18\n\x10valid_thru_month\x18\x04 \x01(\x05\x12\x17\n\x0fvalid_thru_year\x18\x05 \x01(\x05\x12\x13\n\x0btotal_price\x18\x06 \x01(\x02\x12\x1e\n\x06status\x18\x07 \x01(\x0e\x32\x0e.PaymentStatus*K\n\rPaymentStatus\x12\x0b\n\x07PENDING\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\n\n\x06\x46\x41ILED\x10\x02\x12\x0b\n\x07\x44\x45\x43LINE\x10\x03\x12\x07\n\x03\x43OD\x10\x04\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'payment_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PAYMENTSTATUS._serialized_start=190
  _PAYMENTSTATUS._serialized_end=265
  _PAYMENTCREATE._serialized_start=18
  _PAYMENTCREATE._serialized_end=188
# @@protoc_insertion_point(module_scope)