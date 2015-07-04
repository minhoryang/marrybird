"""up/download (currently images only)."""

from base64 import b64encode
from os import path
from datetime import datetime
from urllib.parse import quote

from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app, make_response, request
from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user, JWTError  # TODO: Refactor JWT.

from ._base import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))

    orig_filename = db.Column(db.String(100))  # TODO: is it enough?! :(
    dest_filename = db.Column(db.String(100))
    extension = db.Column(db.String(5))
    mimetype = db.Column(db.String(20))
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
    @api.doc(responses={200:'Successfully Uploaded', 400:'Bad Request', 401:'Auth Failed', 404:'Not Found'})
    class FileUploadByMultipart(Resource):
        wanted = api.parser()
        #wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
        wanted.add_argument('file1', type=FileStorage, required=True, help='.jpg .png', location='files')
        #wanted.add_argument('file2', type=FileStorage, required=True, help='', location='files')  # TODO: Multiple

        #@jwt_required()
        @api.doc(parser=wanted)  # TODO: Content Types
        def post(self, username):
            """Upload your file(s) by multipart format."""
            if False:  #current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400  # TODO: refactor others like this.
            else:
                args = self.wanted.parse_args()
                handled = []
                failed = []
                for arg_name in args:
                    if 'file' in arg_name:
                        if _allowed_file(args[arg_name].filename):
                            dest_filename = secure_filename(str(datetime.now()) + '.' + args[arg_name].filename)
                            # TODO: badly above %s.%s.%s % (a,b,c)
                            # TODO: check magic(file_header)
                            args[arg_name].save(path.join(current_app.config['UPLOAD_FOLDER'], dest_filename))
                            f = File(
                                username=username,
                                orig_filename=args[arg_name].filename,
                                dest_filename=dest_filename,
                                extension=dest_filename.rsplit('.', 1)[1],
                                mimetype=args[arg_name].mimetype
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
        @namespace.route('/<int:idx>')
        @api.doc(response={200:'Successfully Downloaded', 400:'Bad Request', 401:'Auth Failed', 404:'Not Found'})
        class FileDownload(Resource):
            wanted = api.parser()
            wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

            @jwt_required()
            @api.doc(parser=wanted, description="Checkout the chrome debug browser - Network sections.\n"
                                                "(Below image can't loaded because they reload without an authorizaion header.\n"
                                                "But you can download it directly.)")
            def get(self, idx):
                """Download file. (without approval check) (but checked the user)"""  # TODO: APPROVAL CHECK!
                f = File.query.get(idx)
                if not f:
                    return {'status': 404, 'message': 'Not Found'}, 404
                else:
                    response = make_response(open(path.join(current_app.config['UPLOAD_FOLDER'], f.dest_filename), 'rb').read())
                    response.content_type = f.mimetype
                    return response

            # XXX : Not Worked at Web UI.
            """
            wanted2 = api.parser()
            wanted2.add_argument('bearer', type=str, required=True, help='"$JsonWebToken"', location='form')
            @api.doc(parser=wanted2)
            def post(self, idx):
                args = self.wanted2.parse_args()
                return BearerDownloader(idx, args['bearer'])
            """

        @namespace.route('/<int:idx>/base64')
        @api.doc(response={200:'Successfully Downloaded', 400:'Bad Request', 401:'Auth Failed', 404:'Not Found'})
        class FileDownloadBase64(Resource):
            wanted = api.parser()
            wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

            @jwt_required()
            @api.doc(parser=wanted, description="1. Copy below base64 strings at 'message'\n"
                                                "2. Launch new blank page (about:blank)\n"
                                                "3. \<img src=\'PASTE_IT_HERE\'/\>")
            def get(self, idx):
                """Download file. (without approval check) (but checked the user)"""  # TODO: APPROVAL CHECK!
                f = File.query.get(idx)
                if not f:
                    return {'status': 404, 'message': 'Not Found'}, 404
                else:
                    base64 = b64encode(open(path.join(current_app.config['UPLOAD_FOLDER'], f.dest_filename), 'rb').read())
                    return {'status': 200, 'message': 'data:%s;base64,%s' % (f.mimetype, quote(base64))}

        """
        @namespace.route('/<int:idx>/base64_tester')
        @api.representation('text/html')
        class FileDownloadBase64_Tester(Resource):
            wanted = api.parser()
            wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

            @api.doc(parser=wanted)
            def get(self, idx):
                args = self.wanted.parse_args()
                # TODO
                response = make_response("<html><body><script src='//code.jquery.com/jquery-2.1.4.min.js'/><img><script></script></body></html>")
                response.content_type = "text/html"
                return response  # redirect?!
        """

        @namespace.route('/<int:idx>/<string:bearer>')
        @api.doc(response={200:'Successfully Downloaded', 400:'Bad Request', 401:'Auth Failed', 404:'Not Found'})
        class FileDownloadBase64_QueryString(Resource):
            def get(self, idx, bearer):
                return BearerDownloader(idx, bearer)

    def BearerDownloader(idx, bearer):
        try:
            payload = jwt.decode_callback(bearer)
            user = jwt.user_callback(payload)
        except JWTError:
            return {'status': 401, 'message': 'Auth Failed'}, 401
        else:
            f = File.query.get(idx)
            if not f:
                return {'status': 404, 'message': 'Not Found'}, 404
            else:
                response = make_response(open(path.join(current_app.config['UPLOAD_FOLDER'], f.dest_filename), 'rb').read())
                response.content_type = f.mimetype
                return response