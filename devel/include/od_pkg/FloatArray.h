// Generated by gencpp from file od_pkg/FloatArray.msg
// DO NOT EDIT!


#ifndef OD_PKG_MESSAGE_FLOATARRAY_H
#define OD_PKG_MESSAGE_FLOATARRAY_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <od_pkg/FloatList.h>

namespace od_pkg
{
template <class ContainerAllocator>
struct FloatArray_
{
  typedef FloatArray_<ContainerAllocator> Type;

  FloatArray_()
    : lists()  {
    }
  FloatArray_(const ContainerAllocator& _alloc)
    : lists(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector< ::od_pkg::FloatList_<ContainerAllocator> , typename std::allocator_traits<ContainerAllocator>::template rebind_alloc< ::od_pkg::FloatList_<ContainerAllocator> >> _lists_type;
  _lists_type lists;





  typedef boost::shared_ptr< ::od_pkg::FloatArray_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::od_pkg::FloatArray_<ContainerAllocator> const> ConstPtr;

}; // struct FloatArray_

typedef ::od_pkg::FloatArray_<std::allocator<void> > FloatArray;

typedef boost::shared_ptr< ::od_pkg::FloatArray > FloatArrayPtr;
typedef boost::shared_ptr< ::od_pkg::FloatArray const> FloatArrayConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::od_pkg::FloatArray_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::od_pkg::FloatArray_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::od_pkg::FloatArray_<ContainerAllocator1> & lhs, const ::od_pkg::FloatArray_<ContainerAllocator2> & rhs)
{
  return lhs.lists == rhs.lists;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::od_pkg::FloatArray_<ContainerAllocator1> & lhs, const ::od_pkg::FloatArray_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace od_pkg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::od_pkg::FloatArray_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::od_pkg::FloatArray_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::od_pkg::FloatArray_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::od_pkg::FloatArray_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::od_pkg::FloatArray_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::od_pkg::FloatArray_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::od_pkg::FloatArray_<ContainerAllocator> >
{
  static const char* value()
  {
    return "640e948749c147faa7ff8fdc76d0987c";
  }

  static const char* value(const ::od_pkg::FloatArray_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x640e948749c147faULL;
  static const uint64_t static_value2 = 0xa7ff8fdc76d0987cULL;
};

template<class ContainerAllocator>
struct DataType< ::od_pkg::FloatArray_<ContainerAllocator> >
{
  static const char* value()
  {
    return "od_pkg/FloatArray";
  }

  static const char* value(const ::od_pkg::FloatArray_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::od_pkg::FloatArray_<ContainerAllocator> >
{
  static const char* value()
  {
    return "FloatList[] lists\n"
"\n"
"================================================================================\n"
"MSG: od_pkg/FloatList\n"
"float64[] elements\n"
;
  }

  static const char* value(const ::od_pkg::FloatArray_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::od_pkg::FloatArray_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.lists);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FloatArray_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::od_pkg::FloatArray_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::od_pkg::FloatArray_<ContainerAllocator>& v)
  {
    s << indent << "lists[]" << std::endl;
    for (size_t i = 0; i < v.lists.size(); ++i)
    {
      s << indent << "  lists[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::od_pkg::FloatList_<ContainerAllocator> >::stream(s, indent + "    ", v.lists[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // OD_PKG_MESSAGE_FLOATARRAY_H
