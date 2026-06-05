// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from task3:srv/PrimeFactors.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "task3/srv/prime_factors.h"


#ifndef TASK3__SRV__DETAIL__PRIME_FACTORS__STRUCT_H_
#define TASK3__SRV__DETAIL__PRIME_FACTORS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/PrimeFactors in the package task3.
typedef struct task3__srv__PrimeFactors_Request
{
  uint8_t structure_needs_at_least_one_member;
} task3__srv__PrimeFactors_Request;

// Struct for a sequence of task3__srv__PrimeFactors_Request.
typedef struct task3__srv__PrimeFactors_Request__Sequence
{
  task3__srv__PrimeFactors_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} task3__srv__PrimeFactors_Request__Sequence;

// Constants defined in the message

/// Struct defined in srv/PrimeFactors in the package task3.
typedef struct task3__srv__PrimeFactors_Response
{
  uint8_t structure_needs_at_least_one_member;
} task3__srv__PrimeFactors_Response;

// Struct for a sequence of task3__srv__PrimeFactors_Response.
typedef struct task3__srv__PrimeFactors_Response__Sequence
{
  task3__srv__PrimeFactors_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} task3__srv__PrimeFactors_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  task3__srv__PrimeFactors_Event__request__MAX_SIZE = 1
};
// response
enum
{
  task3__srv__PrimeFactors_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/PrimeFactors in the package task3.
typedef struct task3__srv__PrimeFactors_Event
{
  service_msgs__msg__ServiceEventInfo info;
  task3__srv__PrimeFactors_Request__Sequence request;
  task3__srv__PrimeFactors_Response__Sequence response;
} task3__srv__PrimeFactors_Event;

// Struct for a sequence of task3__srv__PrimeFactors_Event.
typedef struct task3__srv__PrimeFactors_Event__Sequence
{
  task3__srv__PrimeFactors_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} task3__srv__PrimeFactors_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TASK3__SRV__DETAIL__PRIME_FACTORS__STRUCT_H_
