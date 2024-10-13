; Auto-generated. Do not edit!


(cl:in-package od_pkg-msg)


;//! \htmlinclude FloatList.msg.html

(cl:defclass <FloatList> (roslisp-msg-protocol:ros-message)
  ((elements
    :reader elements
    :initarg :elements
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass FloatList (<FloatList>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatList>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatList)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name od_pkg-msg:<FloatList> is deprecated: use od_pkg-msg:FloatList instead.")))

(cl:ensure-generic-function 'elements-val :lambda-list '(m))
(cl:defmethod elements-val ((m <FloatList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader od_pkg-msg:elements-val is deprecated.  Use od_pkg-msg:elements instead.")
  (elements m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatList>) ostream)
  "Serializes a message object of type '<FloatList>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'elements))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'elements))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatList>) istream)
  "Deserializes a message object of type '<FloatList>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'elements) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'elements)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatList>)))
  "Returns string type for a message object of type '<FloatList>"
  "od_pkg/FloatList")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatList)))
  "Returns string type for a message object of type 'FloatList"
  "od_pkg/FloatList")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatList>)))
  "Returns md5sum for a message object of type '<FloatList>"
  "1bc954623d5640da8f69f8b82a598854")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatList)))
  "Returns md5sum for a message object of type 'FloatList"
  "1bc954623d5640da8f69f8b82a598854")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatList>)))
  "Returns full string definition for message of type '<FloatList>"
  (cl:format cl:nil "float64[] elements~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatList)))
  "Returns full string definition for message of type 'FloatList"
  (cl:format cl:nil "float64[] elements~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatList>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'elements) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatList>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatList
    (cl:cons ':elements (elements msg))
))
