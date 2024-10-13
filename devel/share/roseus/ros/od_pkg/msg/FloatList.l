;; Auto-generated. Do not edit!


(when (boundp 'od_pkg::FloatList)
  (if (not (find-package "OD_PKG"))
    (make-package "OD_PKG"))
  (shadow 'FloatList (find-package "OD_PKG")))
(unless (find-package "OD_PKG::FLOATLIST")
  (make-package "OD_PKG::FLOATLIST"))

(in-package "ROS")
;;//! \htmlinclude FloatList.msg.html


(defclass od_pkg::FloatList
  :super ros::object
  :slots (_elements ))

(defmethod od_pkg::FloatList
  (:init
   (&key
    ((:elements __elements) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _elements __elements)
   self)
  (:elements
   (&optional __elements)
   (if __elements (setq _elements __elements)) _elements)
  (:serialization-length
   ()
   (+
    ;; float64[] _elements
    (* 8    (length _elements)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _elements
     (write-long (length _elements) s)
     (dotimes (i (length _elements))
       (sys::poke (elt _elements i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _elements
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _elements (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _elements i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get od_pkg::FloatList :md5sum-) "1bc954623d5640da8f69f8b82a598854")
(setf (get od_pkg::FloatList :datatype-) "od_pkg/FloatList")
(setf (get od_pkg::FloatList :definition-)
      "float64[] elements

")



(provide :od_pkg/FloatList "1bc954623d5640da8f69f8b82a598854")


