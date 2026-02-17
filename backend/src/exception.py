import sys ##Used to access: sys.exc_info() → gives exception details
from src.logger import logging

def error_message_details(error,error_detail:sys):  ##error → the original exception, error_detail → system info (sys)
    _,_,exc_tb=error_detail.exc_info()  ##_ → exception type (ignored), _ → exception value (ignored), exc_tb → traceback object (important)
    file_name=exc_tb.tb_frame.f_code.co_filename ##Tells you which Python file caused the error.
    error_message="Error occured in python script name [{0}] line number [{1}] error_message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)

    )
    return error_message

class CustomException(Exception):   ## You’re creating your own exception type.
    def __init__(self,error_message,error_detail:sys):   ## Intended to: Call parent Exception, Store detailed error message
        super().__init__(error_message) ## So when you print the exception, you get the detailed message.
        self.error_message=error_message_details(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message



if __name__=="__main__":

    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero error")
        raise CustomException(e, sys)