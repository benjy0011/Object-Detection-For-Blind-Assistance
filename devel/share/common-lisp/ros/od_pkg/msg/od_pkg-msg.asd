
(cl:in-package :asdf)

(defsystem "od_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "FloatArray" :depends-on ("_package_FloatArray"))
    (:file "_package_FloatArray" :depends-on ("_package"))
    (:file "FloatList" :depends-on ("_package_FloatList"))
    (:file "_package_FloatList" :depends-on ("_package"))
  ))