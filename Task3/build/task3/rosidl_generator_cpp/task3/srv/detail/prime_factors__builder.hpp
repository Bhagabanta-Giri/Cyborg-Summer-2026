// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from task3:srv/PrimeFactors.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "task3/srv/prime_factors.hpp"


#ifndef TASK3__SRV__DETAIL__PRIME_FACTORS__BUILDER_HPP_
#define TASK3__SRV__DETAIL__PRIME_FACTORS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "task3/srv/detail/prime_factors__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace task3
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::task3::srv::PrimeFactors_Request>()
{
  return ::task3::srv::PrimeFactors_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace task3


namespace task3
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::task3::srv::PrimeFactors_Response>()
{
  return ::task3::srv::PrimeFactors_Response(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace task3


namespace task3
{

namespace srv
{

namespace builder
{

class Init_PrimeFactors_Event_response
{
public:
  explicit Init_PrimeFactors_Event_response(::task3::srv::PrimeFactors_Event & msg)
  : msg_(msg)
  {}
  ::task3::srv::PrimeFactors_Event response(::task3::srv::PrimeFactors_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::task3::srv::PrimeFactors_Event msg_;
};

class Init_PrimeFactors_Event_request
{
public:
  explicit Init_PrimeFactors_Event_request(::task3::srv::PrimeFactors_Event & msg)
  : msg_(msg)
  {}
  Init_PrimeFactors_Event_response request(::task3::srv::PrimeFactors_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_PrimeFactors_Event_response(msg_);
  }

private:
  ::task3::srv::PrimeFactors_Event msg_;
};

class Init_PrimeFactors_Event_info
{
public:
  Init_PrimeFactors_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PrimeFactors_Event_request info(::task3::srv::PrimeFactors_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_PrimeFactors_Event_request(msg_);
  }

private:
  ::task3::srv::PrimeFactors_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::task3::srv::PrimeFactors_Event>()
{
  return task3::srv::builder::Init_PrimeFactors_Event_info();
}

}  // namespace task3

#endif  // TASK3__SRV__DETAIL__PRIME_FACTORS__BUILDER_HPP_
