#include "ContextParameters.h"
#include "moses/Util.h"

namespace Moses
{

ContextParameters::
ContextParameters()
  : look_ahead(0), look_back(0) { }

void
ContextParameters::
init(Parameter& params)
{
  look_back = look_ahead = 0;
  params.SetParameter(context_string, "context-string", std::string(""));
  std::string context_window;
  params.SetParameter(context_window, "context-window", std::string(""));

  if (context_window == "") 
    return;

  size_t p = context_window.find_first_of("0123456789");
  if (p == 0) 
    look_back = look_ahead = atoi(context_window.c_str());
  if (p == 1) 
    {
      if (context_window[0] == '-') 
	look_back  = atoi(context_window.substr(1).c_str());
      else if (context_window[0] == '+') 
	look_ahead = atoi(context_window.substr(1).c_str());
      else
	UTIL_THROW2("Invalid specification of context window.");
    }
  if (p == 2) 
    {
      if (context_window.substr(0,2) == "+-" ||
	  context_window.substr(0,2) == "-+")
	look_back = look_ahead = atoi(context_window.substr(p).c_str());
      else 
	UTIL_THROW2("Invalid specification of context window.");
    }
}
}
