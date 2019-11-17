import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

from .model import StrukturOrganisasi
from blueprints import db, app
from sqlalchemy import desc
# 'client' penamaan (boleh diganti)

bp_strukturOrganisasi = Blueprint('strukturOrganisasi', __name__)
api = Api(bp_strukturOrganisasi)


class StrukturOrganisasiResource(Resource):

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',location='args', help='invalid id', required=True)
        args = parser.parse_args()

        qry = StrukturOrganisasi.query.get(args["id"])

        if qry is not None:
            return {"status":"success", "result":marshal(qry, StrukturOrganisasi.response_field)}, 200, {'Content-Type':'application/json'}

        return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}


    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_organisasi',location='json', help='invalid nama_organisasi', required=True)
        parser.add_argument('induk_organisasi',location='json', help='invalid induk_organisasi', required=True)
        parser.add_argument('alamat',location='json', help='invalid alamat')
        parser.add_argument('kabupaten',location='json', help='invalid kabupaten', required=True)
        parser.add_argument('kecamatan',location='json', help='invalid kecamatan', required=True)
        parser.add_argument('desa',location='json', help='invalid desa', required=True)
        parser.add_argument('no_telepon',location='json', help='invalid no_telepon')
        parser.add_argument('email',location='json', help='invalid email')
        parser.add_argument('kontak_person',location='json', help='invalid kontak_person')
        args = parser.parse_args()
        
        claims = get_jwt_claims()

        qry = StrukturOrganisasi(datetime.datetime.now(), args['nama_organisasi'], args['induk_organisasi'],args['alamat'], args['kabupaten'],args['kecamatan'],args['desa'],args['no_telepon'],args['email'],args['kontak_person'],claims['id'])

        db.session.add(qry)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', qry)

        return {"status":"success", "result":marshal(qry, StrukturOrganisasi.response_field)}, 200, {'Content-Type':'application/json'}

    @jwt_required
    @internal_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_organisasi',location='json', help='invalid nama_organisasi', required=True)
        parser.add_argument('induk_organisasi',location='json', help='invalid induk_organisasi', required=True)
        parser.add_argument('alamat',location='json', help='invalid alamat')
        parser.add_argument('kabupaten',location='json', help='invalid kabupaten', required=True)
        parser.add_argument('kecamatan',location='json', help='invalid kecamatan', required=True)
        parser.add_argument('desa',location='json', help='invalid desa', required=True)
        parser.add_argument('no_telepon',location='json', help='invalid no_telepon')
        parser.add_argument('email',location='json', help='invalid email')
        parser.add_argument('kontak_person',location='json', help='invalid kontak_person')
        parser.add_argument('id',location='args', help='invalid id', required=True)
        args = parser.parse_args()

        qry = StrukturOrganisasi.query.get(args["id"])

        if qry is None:
            return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}

        qry.nama_organisasi = args['nama_organisasi']
        qry.induk_organisasi = args['induk_organisasi']
        qry.alamat = args['alamat']
        qry.kabupaten = args['kabupaten']
        qry.kecamatan = args['kecamatan']
        qry.desa = args['desa']
        qry.no_telepon = args['no_telepon']
        qry.email = args['email']
        qry.kontak_person = args['kontak_person']
        db.session.commit()

        return {"status":"success", "result":marshal(qry, StrukturOrganisasi.response_field)}, 200, {'Content-Type':'application/json'}

    
    @jwt_required
    @internal_required
    def delete(self):
        return {"status":"failed", "result":"Delete Not Available Now, Please Contact Developer"}, 403, {'Content-Type':'application/json'}
        
        parser = reqparse.RequestParser()
        parser.add_argument('id',location='json', help='invalid id', required=True)
        args = parser.parse_args()

        qry = StrukturOrganisasi.query.get(args["id"])

        if qry is None:
            return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {"status":"success", "result":marshal(qry, StrukturOrganisasi.response_field)}, 200, {'Content-Type':'application/json'}

class StrukturOrganisasiResourceList(Resource):

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('id',type=int,location='args', help='invalid book id')
        parser.add_argument('kabupaten',location='args', help='invalid isbn')
        parser.add_argument('kecamatan',location='args', help='invalid isbn')
        parser.add_argument('desa',location='args', help='invalid isbn')
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = StrukturOrganisasi.query

        if args['id'] is not None:
            qry = qry.filter_by(id=args['id'])

        if args['kabupaten'] is not None:
            qry = qry.filter_by(kabupaten=args['kabupaten'])

        if args['kecamatan'] is not None:
            qry = qry.filter_by(kecamatan=args['kecamatan'])

        if args['desa'] is not None:
            qry = qry.filter_by(desa=args['desa'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row, StrukturOrganisasi.response_field))
        
        results = {}
        results['page'] = args['p']
        results['total_page'] = len(result) // args['rp'] +1
        results['per_page'] = args['rp']
        results['data'] = result
        
        return {"status":"success", "result":results}, 200, {'Content-Type':'application/json'}

api.add_resource(StrukturOrganisasiResource, '','')
api.add_resource(StrukturOrganisasiResourceList, '/list')

