;; Auto-generated. Do not edit!


(when (boundp 'od_pkg::FloatArray)
  (if (not (find-package "OD_PKG"))
    (make-package "OD_PKG"))
  (shadow 'FloatArray (find-package "OD_PKG")))
(unless (find-package "OD_PKG::FLOATARRAY")
  (make-package "OD_PKG::FLOATARRAY"))

(in-package "ROS")
;;//! \htmlinclude FloatArray.msg.html


(defclass od_pkg::FloatArray
  :super ros::object
  :slots (_lists ))

(defmethod od_pkg::FloatArray
  (:init
   (&key
    ((:lists __lists) (let (r) (dotimes (i 0) (push (instance od_pkg::FloatList :init) r)) r))
    )
   (send-super :init)
   (setq _lists __lists)
   self)
  (:lists
   (&rest __lists)
   (if (keywordp (car __lists))
       (send* _lists __lists)
     (progn
       (if __lists (setq _lists (car __lists)))
       _lists)))
  (:serialization-length
   ()
   (+
    ;; od_pkg/FloatList[] _lists
    (apply #'+ (send-all _lists :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; od_pkg/FloatList[] _lists
     (write-long (length _lists) s)
     (dolist (elem _lists)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; od_pkg/FloatList[] _lists
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _lists (let (r) (dotimes (i n) (push (instance od_pkg::FloatList :init) r)) r))
     (dolist (elem- _lists)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get od_pkg::FloatArray :md5sum-) "640e948749c147faa7ff8fdc76d0987c")
(setf (get od_pkg::FloatArray :datatype-) "od_pkg/FloatArray")
(setf (get od_pkg::FloatArray :definition-)
      "FloatList[] lists

================================================================================
MSG: od_pkg/FloatList
float64[] elements

")



(provide :od_pkg/FloatArray "640e948749c147faa7ff8fdc76d0987c")


