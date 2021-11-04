#!/usr/bin/env python3
# Autor @kaosxx88
# class worket to interact with Qt multy threading

from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, pyqtSlot
import traceback
import sys 

class WorkerSignals(QObject):

    finished    = pyqtSignal() 
    error       = pyqtSignal(tuple)
    result      = pyqtSignal(object)
    progress    = pyqtSignal(str)


class Ui_worker(QRunnable):


    def __init__(self, fn_or_class, fn_or_class_name, *args, **kwargs):
        super(Ui_worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn_or_class = fn_or_class
        self.fn_or_class_name = fn_or_class_name
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):

        try:

            if self.fn_or_class_name == 'Pmx3_read_keys_from_desfire':

                desfire = self.fn_or_class(*self.args, **self.kwargs)
                result = (desfire.error, desfire.private_key , desfire.public_key)

            elif self.fn_or_class_name == 'Client_registration':


                user_check_registration = self.fn_or_class(*self.args, **self.kwargs)


                result = user_check_registration.return_value()


            else:
                result = self.fn_or_class(*self.args, **self.kwargs)

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        else:
            self.signals.result.emit(result)  

        finally:
            self.signals.finished.emit()  