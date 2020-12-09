# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: module.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='module.proto',
  package='module',
  syntax='proto3',
  serialized_options=b'\n\033com.nanum.grpc.proto.moduleB\013ModuleProtoP\001\242\002\005NANUM',
  serialized_pb=b'\n\x0cmodule.proto\x12\x06module\"\x16\n\x07Request\x12\x0b\n\x03str\x18\x01 \x01(\t\"\x14\n\x05Reply\x12\x0b\n\x03str\x18\x01 \x01(\t27\n\x06Module\x12-\n\trunModule\x12\x0f.module.Request\x1a\r.module.Reply\"\x00\x42\x34\n\x1b\x63om.nanum.grpc.proto.moduleB\x0bModuleProtoP\x01\xa2\x02\x05NANUMb\x06proto3'
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='module.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='str', full_name='module.Request.str', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=46,
)


_REPLY = _descriptor.Descriptor(
  name='Reply',
  full_name='module.Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='str', full_name='module.Reply.str', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=68,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Reply'] = _REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'module_pb2'
  # @@protoc_insertion_point(class_scope:module.Request)
  })
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'module_pb2'
  # @@protoc_insertion_point(class_scope:module.Reply)
  })
_sym_db.RegisterMessage(Reply)


DESCRIPTOR._options = None

_MODULE = _descriptor.ServiceDescriptor(
  name='Module',
  full_name='module.Module',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=70,
  serialized_end=125,
  methods=[
  _descriptor.MethodDescriptor(
    name='runModule',
    full_name='module.Module.runModule',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_REPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MODULE)

DESCRIPTOR.services_by_name['Module'] = _MODULE

# @@protoc_insertion_point(module_scope)
