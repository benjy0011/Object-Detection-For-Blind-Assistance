; Auto-generated. Do not edit!


(cl:in-package od_pkg-msg)


;//! \htmlinclude FloatArray.msg.html

(cl:defclass <FloatArray> (roslisp-msg-protocol:ros-message)
  ((lists
    :reader lists
    :initarg :lists
    :type (cl:vector od_pkg-msg:FloatList)
   :initform (cl:make-array 0 :element-type 'od_pkg-msg:FloatList :initial-element (cl:make-instance 'od_pkg-msg:FloatList))))
)

(cl:defclass FloatArray (<FloatArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name od_pkg-msg:<FloatArray> is deprecated: use od_pkg-msg:FloatArray instead.")))

(cl:ensure-generic-function 'lists-val :lambda-list '(m))
(cl:defmethod lists-val ((m <FloatArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader od_pkg-msg:lists-val is deprecated.  Use od_pkg-msg:lists instead.")
  (lists m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatArray>) ostream)
  "Serializes a message object of type '<FloatArray>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'lists))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'lists))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatArray>) istream)
  "Deserializes a message object of type '<FloatArray>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'lists) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'lists)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'od_pkg-msg:FloatList))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatArray>)))
  "Returns string type for a message object of type '<FloatArray>"
  "od_pkg/FloatArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray)))
  "Returns string type for a message object of type 'FloatArray"
  "od_pkg/FloatArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatArray>)))
  "Returns md5sum for a message object of type '<FloatArray>"
  "640e948749c147faa7ff8fdc76d0987c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatArray)))
  "Returns md5sum for a message object of type 'FloatArray"
  "640e948749c147faa7ff8fdc76d0987c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatArray>)))
  "Returns full string definition for message of type '<FloatArray>"
  (cl:format cl:nil "FloatList[] lists~%~%================================================================================~%MSG: od_pkg/FloatList~%float64[] elements~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatArray)))
  "Returns full string definition for message of type 'FloatArray"
  (cl:format cl:nil "FloatList[] lists~%~%================================================================================~%MSG: od_pkg/FloatList~%float64[] elements~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatArray>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'lists) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatArray>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatArray
    (cl:cons ':lists (lists msg))
))
