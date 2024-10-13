// Auto-generated. Do not edit!

// (in-package od_pkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let FloatList = require('./FloatList.js');

//-----------------------------------------------------------

class FloatArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.lists = null;
    }
    else {
      if (initObj.hasOwnProperty('lists')) {
        this.lists = initObj.lists
      }
      else {
        this.lists = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type FloatArray
    // Serialize message field [lists]
    // Serialize the length for message field [lists]
    bufferOffset = _serializer.uint32(obj.lists.length, buffer, bufferOffset);
    obj.lists.forEach((val) => {
      bufferOffset = FloatList.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type FloatArray
    let len;
    let data = new FloatArray(null);
    // Deserialize message field [lists]
    // Deserialize array length for message field [lists]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.lists = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.lists[i] = FloatList.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.lists.forEach((val) => {
      length += FloatList.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'od_pkg/FloatArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '640e948749c147faa7ff8fdc76d0987c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    FloatList[] lists
    
    ================================================================================
    MSG: od_pkg/FloatList
    float64[] elements
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new FloatArray(null);
    if (msg.lists !== undefined) {
      resolved.lists = new Array(msg.lists.length);
      for (let i = 0; i < resolved.lists.length; ++i) {
        resolved.lists[i] = FloatList.Resolve(msg.lists[i]);
      }
    }
    else {
      resolved.lists = []
    }

    return resolved;
    }
};

module.exports = FloatArray;
