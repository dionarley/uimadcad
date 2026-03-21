
if __name__ == '__main__':

	# import the minimal runtime before checks
	import sys, os, locale

	import madcad
	from madcad.qt import (
		Qt, QTimer,
		QIcon,
		QApplication, QErrorMessage, QMessageBox,
		)
	
	from uimadcad import version, settings, resourcedir
	from uimadcad.utils import *
	from uimadcad.app import Madcad
	
	# set process name
	if sys.platform == 'linux':
		from ctypes import cdll, byref, create_string_buffer
		newname = b'madcad'
		libc = cdll.LoadLibrary('libc.so.6')
		buff = create_string_buffer(len(newname)+1)
		buff.value = newname
		libc.prctl(15, byref(buff), 0, 0, 0)
	
	# parse commandline arguments
	file = None
	if len(sys.argv) >= 2:
		file = sys.argv[1]
	
	# # limit numpy threads (because it is using ways too much when solving kinematic
	# os.environ["OMP_NUM_THREADS"] = "2"
	# os.environ["OPENBLAS_NUM_THREADS"] = "2"
	# os.environ["MKL_NUM_THREADS"] = "2"
	# os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
	# os.environ["NUMEXPR_NUM_THREADS"] = "2"

	
	# set Qt opengl context sharing to avoid reinitialization of scenes everytime, (this is for pymadcad display)
	QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
	# setup Qt application
	app = QApplication(sys.argv)
	app.setApplicationName('madcad')
	app.setApplicationVersion(version)
	app.setApplicationDisplayName('madcad v{}'.format(version))
	
	# set icons as not always provided by the system
	path = QIcon.themeSearchPaths()
	path.append(resourcedir + '/icons')
	QIcon.setThemeSearchPaths(path)
	QIcon.setThemeName('breeze')
	
	madcad.settings.install()
	madcad.settings.load()
	settings.install()
	settings.load()
	settings.use_color_preset()
	settings.use_stylesheet()
	
	# set locale settings to C default to get correct 'repr' of glm types
	locale.setlocale(locale.LC_NUMERIC, 'C')
	
	# create or load config
	if madcad.settings.display['system_theme']:
		madcad.settings.use_qt_colors()
	if settings.scriptview['system_theme']:
		settings.use_qt_colors()
	
	# limit the number of cores that numpy is using, to prefent it to take all the cpu to uselessly parallelize simple operations
	from threadpoolctl import threadpool_limits
	with threadpool_limits(limits=1, user_api='blas'):
	
		# start software
		madcad = Madcad(file)
	
	qtmain(app)
