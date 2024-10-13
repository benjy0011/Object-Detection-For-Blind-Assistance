// Generated by gencpp from file od_pkg/FloatList.msg
// DO NOT EDIT!


#ifndef OD_PKG_MESSAGE_FLOATLIST_H
#define OD_PKG_MESSAGE_FLOATLIST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace od_pkg
{
template <class ContainerAllocator>
struct FloatList_
{
  typedef FloatList_<ContainerAllocator> Type;

  FloatList_()
    : elements()  {
    }
  FloatList_(const ContainerAllocator& _alloc)
    : elements(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> _elements_type;
  _elements_type elements;





  typedef boost::shared_ptr< ::od_pkg::FloatList_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::od_pkg::FloatList_<ContainerAllocator> const> ConstPtr;

}; // struct FloatList_

typedef ::od_pkg::FloatList_<std::allocator<void> > FloatList;

typedef boost::shared_ptr< ::od_pkg::FloatList > FloatListPtr;
typedef boost::shared_ptr< ::od_pkg::FloatList const> FloatListConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::od_pkg::FloatList_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::od_pkg::FloatList_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::od_pkg::FloatList_<ContainerAllocator1> & lhs, const ::od_pkg::FloatList_<ContainerAllocator2> & rhs)
{
  return lhs.elements == rhs.elements;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::od_pkg::FloatList_<ContainerAllocator1> & lhs, const ::od_pkg::FloatList_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace od_pkg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::od_pkg::FloatList_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::od_pkg::FloatList_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::od_pkg::FloatList_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::od_pkg::FloatList_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::od_pkg::FloatList_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::od_pkg::FloatList_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::od_pkg::FloatList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "1bc954623d5640da8f69f8b82a598854";
  }

  static const char* value(const ::od_pkg::FloatList_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x1bc954623d5640daULL;
  static const uint64_t static_value2 = 0x8f69f8b82a598854ULL;
};

template<class ContainerAllocator>
struct DataType< ::od_pkg::FloatList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "od_pkg/FloatList";
  }

  static const char* value(const ::od_pkg::FloatList_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::od_pkg::FloatList_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64[] elements\n"
;
  }

  static const char* value(const ::od_pkg::FloatList_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::od_pkg::FloatList_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.elements);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FloatList_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::od_pkg::FloatList_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::od_pkg::FloatList_<ContainerAllocator>& v)
  {
    s << indent << "elements[]" << std::endl;
    for (size_t i = 0; i < v.elements.size(); ++i)
    {
      s << indent << "  elements[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.elements[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // OD_PKG_MESSAGE_FLOATLIST_H
