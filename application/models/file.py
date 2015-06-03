"""up/download (currently images only)."""

from os import path
from datetime import datetime

from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app
from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user  # TODO: Refactor JWT.

from ._base import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))

    orig_filename = db.Column(db.String(100))  # TODO: is it enough?! :(
    dest_filename = db.Column(db.String(100))
    extension = db.Column(db.String(5))
    # md5 = db.Column(db.String(32))  # TODO: add MD5
    # TODO: add Descriptions of file (is this face included?)
    # TODO: add GraphicHash


def init(api, jwt):
    """."""
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    """TODO: Refactor JWT.
        /<string:username> -> /<jwt:key>/image.png (.jpg)

        Invoke new image key per image request.
        ex)
        1. I uploaded my photo a.png.
        2. If you want to see my photo a.png? No, You don't have a key.
        3. If system thinks You and I can be a quite good friend?
           Then system generate new JWT key for reading a.png by you.
        4. You asked to download a.png with above key.
        5. PROFIT!
    """

    def _allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['jpg', 'png']

    @namespace.route('/<string:username>')  # TODO: REGEX .jpg, .png
    @api.doc(responses={200:'Successfully Login', 400:'Bad Request', 401:'Auth Failed', 404:'Not Found'})
    class FileUploadByMultipart(Resource):
        wanted = api.parser()
        wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
        wanted.add_argument('file1', type=FileStorage, required=True, help='.jpg .png', location='files')
        #wanted.add_argument('file2', type=FileStorage, required=True, help='', location='files')  # TODO: Multiple

        @jwt_required()
        @api.doc(parser=wanted)  # TODO: Content Types
        def post(self, username):
            """Upload your file(s) by multipart format."""
            if current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400  # TODO: refactor others like this.
            else:
                args = self.wanted.parse_args()
                handled = []
                failed = []
                for arg_name in args:
                    if 'file' in arg_name:
                        if _allowed_file(args[arg_name].filename):
                            dest_filename = secure_filename(str(datetime.now()) + '.' + str(current_user.id) + '.' + args[arg_name].filename)
                            # TODO: badly above %s.%s.%s % (a,b,c)
                            # TODO: check magic(file_header)
                            args[arg_name].save(path.join(current_app.config['UPLOAD_FOLDER'], dest_filename))
                            f = File(
                                username=username,
                                orig_filename=args[arg_name].filename,
                                dest_filename=dest_filename,
                                extension=dest_filename.rsplit('.', 1)[1]
                            )
                            db.session.add(f)
                            db.session.commit()  # XXX: is it okay to go here?
                            handled.append(f)
                        else:
                            failed.append(args[arg_name].filename)
                    # Others such as authorization(included at parser), file2(not included (yet)) ignored automatically.
                if not failed:
                    return {'status': 200, 'message': [f.id for f in handled]}
                else:
                    return {'status': 400, 'message': 'Not allowed file(s): ' + ', '.join(failed)}, 400

        # GET?!
