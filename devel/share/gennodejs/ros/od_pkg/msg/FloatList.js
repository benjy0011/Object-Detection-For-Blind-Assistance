// Auto-generated. Do not edit!

// (in-package od_pkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class FloatList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.elements = null;
    }
    else {
      if (initObj.hasOwnProperty('elements')) {
        this.elements = initObj.elements
      }
      else {
        this.elements = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type FloatList
    // Serialize message field [elements]
    bufferOffset = _arraySerializer.float64(obj.elements, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type FloatList
    let len;
    let data = new FloatList(null);
    // Deserialize message field [elements]
    data.elements = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.elements.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'od_pkg/FloatList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '1bc954623d5640da8f69f8b82a598854';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] elements
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new FloatList(null);
    if (msg.elements !== undefined) {
      resolved.elements = msg.elements;
    }
    else {
      resolved.elements = []
    }

    return resolved;
    }
};

module.exports = FloatList;
